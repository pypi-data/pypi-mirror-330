import os
import time
import json
import subprocess
from datetime import datetime,timezone
from tqdm import tqdm
from tinydb import TinyDB, Query
from tinydb.middlewares import CachingMiddleware
from tinydb.storages import JSONStorage
import RPi.GPIO as GPIO
from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE

class GPSData:
    def __init__(self, data):
        self.id = data.get('id')
        self.latitude = data.get('latitude')
        self.longitude = data.get('longitude')
        self.altitude = data.get('altitude')
        self.date_created = data.get('date_created')
       
        
class GPSManager:
    def __init__(self, db_path=None, gpio_pin=20, timeout=300):
        """Initialize GPS Manager."""
        
        if db_path is None:
            home_dir = os.path.expanduser("~/.gps")
            os.makedirs(home_dir, exist_ok=True)  # Create the directory if it doesn't exist
            db_path = os.path.join(home_dir, "gps_data.json")
            
        # Initialize GPIO
        self.gpio_pin = gpio_pin
        self.new_data=None
       

        # # Set working directory to script location
        # self.script_dir = os.path.dirname(os.path.realpath(__file__))
        # os.chdir(self.script_dir)

        # Initialize TinyDB with caching middleware
        self.db = TinyDB(db_path, storage=CachingMiddleware(JSONStorage))
        self.timeout = timeout
    def _setup_gpio(self):
        """Initialize GPIO pin."""
        GPIO.setmode(GPIO.BCM)
        try:
             GPIO.cleanup(self.gpio_pin) 
        except Exception:
            pass
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        # print(f"GPIO {self.gpio_pin} initialized successfully.")
        
    def _setup_gpio_with_retry(self, retries=3, delay=1):
        """Retry GPIO setup up to 'retries' times with a delay between attempts."""
        for attempt in range(1, retries + 1):
            try:
                # print(f"Attempt {attempt}/{retries}: Initializing GPIO {self.gpio_pin}")
                self._setup_gpio()
                return  # Exit the method if successful
            except Exception as e:
                # print(f"Error during GPIO initialization on attempt {attempt}: {e}")
                GPIO.cleanup()
                if attempt < retries:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
        raise RuntimeError(f"Failed to initialize GPIO {self.gpio_pin} after {retries} attempts")

    def set_gpio_low(self):
        """Set GPIO pin to LOW."""
        GPIO.output(self.gpio_pin, GPIO.LOW)
        print("Starting GPS")

    def reset_gpio(self):
        """Reset GPIO pin (set it to HIGH)."""
        GPIO.output(self.gpio_pin, GPIO.HIGH)
        print("GPS Stopped")

    def start_gpsd(self):
        """Start the gpsd service."""
        try:
            subprocess.run(['sudo', 'systemctl', 'start', 'gpsd'], check=True)
            print("gpsd service started.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to start gpsd: {e}")

    def stop_gpsd(self):
        """Stop the gpsd service."""
        try:
            subprocess.run(['sudo', 'systemctl', 'stop', 'gpsd'], check=True)
            print("gpsd service stopped.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to stop gpsd: {e}")

    def get_gps_data(self,progress_callback=None):
        """Fetch GPS data using gpsd with a progress bar."""
        session = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
        print("Waiting for GPS fix...")

        with tqdm(total=self.timeout, desc="Time elapsed", unit="s") as pbar:
            start_time = time.time()
            while time.time() - start_time < self.timeout:
                elapsed = int(time.time() - start_time)
                pbar.n = elapsed
                pbar.last_print_n = elapsed  # Sync progress bar display
                pbar.refresh()
                if progress_callback:
                    progress_callback({
                            "current_progress": pbar.n,
                            "total": pbar.total,
                            "elapsed_time_seconds": round(pbar.elapsed, 2),
                            "description": pbar.desc,
                            "unit": pbar.unit,
                            "start_time": pbar.start_t,
                            "last_print_time": pbar.last_print_t,
                            "last_print_progress": pbar.last_print_n,
                            "rate_units_per_second": round(pbar.format_dict["rate"], 2) if "rate" in pbar.format_dict else None,
                            "postfix": pbar.postfix,
                            "disable": pbar.disable,
                            "percentage_complete": round((pbar.n / pbar.total) * 100, 2) if pbar.total else None
                    })

                try:
                    report = session.next()

                    # Display the current status on the same line
                    if report['class'] == 'SKY':
                        nSat = getattr(report, 'nSat', 0)
                        uSat = getattr(report, 'uSat', 0)
                        pbar.set_postfix_str(f"Satellites: {uSat}/{nSat} used")

                    if report['class'] == 'TPV' and getattr(report, 'mode', 0) >= 2:
                        # Successfully acquired fix
                        data = {
                            'latitude': getattr(report, 'lat', 'n/a'),
                            'longitude': getattr(report, 'lon', 'n/a'),
                            'altitude': getattr(report, 'alt', 'n/a'),
                            'time': getattr(report, 'time', 'n/a'),
                        }
                        pbar.set_postfix_str("GPS Fix Acquired!")
                        pbar.close()
                        print("\nGPS Data:", data)
                        return data

                except KeyError:
                    pbar.set_postfix_str("Waiting for valid data...")
                except StopIteration:
                    pbar.set_postfix_str("GPSD has terminated.")
                    break
                except Exception as e:
                    pbar.set_postfix_str(f"Error: {e}")

                time.sleep(1)

        pbar.close()
        print("\nTimeout reached: Unable to get GPS fix.")
        return None

    def save_gps_data(self, data)->GPSData:
        """Save GPS data to TinyDB with auto-increment ID and date_created."""
        try:
            # Get the last doc_id or start at 1
            metadata = self.db.search(Query().type == 'metadata')
            if metadata:
                last_id = metadata[0]['last_record_id']
            else:
                last_id = 0

            # Add auto-increment ID and date_created
            data['id'] = last_id + 1
            data['date_created'] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

            # Save data to TinyDB
            doc_id = self.db.insert(data)

            # Update metadata with the new last_record_id
            self.db.upsert({'type': 'metadata', 'last_record_id': data['id']}, Query().type == 'metadata')

            # Flush cache to ensure data is saved
            self.db.storage.flush()

            print(f"GPS data saved with id: {data['id']} {data['latitude']}")
            return GPSData(data)
        except Exception as e:
            print(f"Error saving GPS data: {e}")
            return None
    def get_last_known_location(self):
        return self.get_last_gps_data()
    def get_last_gps_data(self):
        """Retrieve the last entered GPS data using the metadata last_record_id."""
        try:
            metadata = self.db.search(Query().type == 'metadata')
            if not metadata:
                print("No last_record_id metadata found.")
                return None

            last_record_id = metadata[0].get('last_record_id')
            if not last_record_id:
                print("last_record_id is missing.")
                return None

            # Retrieve the record with the highest ID
            last_record = self.db.get(Query().id == last_record_id)
            return GPSData(last_record)
        except Exception as e:
            print(f"Error retrieving GPS data: {e}")
            return None

    def run(self,progress_callback=None):
        """Main method to manage GPS process."""
        try:
            self._setup_gpio_with_retry()
            self.set_gpio_low()
            self.start_gpsd()
            self.new_data = self.get_gps_data(progress_callback)

            if self.new_data:
                return self.save_gps_data(self.new_data)
            else:
                print("No GPS data retrieved.")
                return None

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.stop_gpsd()
            self.reset_gpio()
            try:
                GPIO.cleanup(self.gpio_pin) 
            except Exception:
                pass

