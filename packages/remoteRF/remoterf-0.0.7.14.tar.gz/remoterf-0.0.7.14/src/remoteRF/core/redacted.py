# Old reservation stuff (hourly block, non distinct device)
# def fetch_all_devices():
#     response = rpc_client(
#         function_name='ACC:get_dev',
#         args={
#             "un": map_arg(account.username),
#             "pw": map_arg(account.password)
#         }
#     )
#     devices = []
#     # Sort keys using numeric conversion when possible.
#     for key in sorted(response.results.keys(), key=lambda k: int(k) if k.isdigit() else k):
#         devices.append(key)
#     return devices



# def fetch_device_reservations_by_date(device_id: str, date: datetime.date):
#     """
#     Filter all reservations to those for a specific device (by ID, as a string)
#     on the specified date.
#     """
#     all_res = fetch_all_reservations()
#     device_reservations = []
#     for res in all_res:
#         # Convert the stored device_id (an int) to a string for comparison.
#         if str(res['device_id']) == device_id and res['start_time'].date() == date:
#             device_reservations.append((res['start_time'], res['end_time']))
            
#     return device_reservations

# def build_hourly_slots(date: datetime.date, start_hour: int = 0, end_hour: int = 24):
#     """Generate 1-hour time slots for the given date."""
#     slots = []
#     for hour in range(start_hour, end_hour):
#         slot_start = datetime.datetime.combine(date, datetime.time(hour, 0))
#         slot_end = slot_start + datetime.timedelta(hours=1)
#         slots.append((slot_start, slot_end))
#     return slots


# def display_free_slots_all(date: datetime.date):
#     """
#     Display available 1-hour slots aggregated across all devices on a given date.
#     A slot is available if at least one device is free.
#     Omits any slots whose end time is in the past.
#     Returns a tuple (chosen_slot, chosen_device) where chosen_slot is (start_time, end_time)
#     and chosen_device is the ID (converted to int if possible) of an available device,
#     or (None, None) if no valid selection.
#     """
#     devices = fetch_all_devices()
#     # Build a mapping: device id -> its reservations for the specified date.
#     device_reservations = {}
#     for dev in devices:
#         device_reservations[dev] = fetch_device_reservations_by_date(dev, date)
    
#     all_slots = build_hourly_slots(date)
#     now = datetime.datetime.now()
#     available_slots = {}  # key: slot tuple, value: list of available device IDs
#     for slot in all_slots:
#         if slot[1] <= now:
#             continue
#         free_devices = []
#         for dev in devices:
#             if not is_slot_conflicting(slot, device_reservations[dev]):
#                 free_devices.append(dev)
#         if free_devices:
#             available_slots[slot] = free_devices

#     if not available_slots:
#         print("No available time slots for any device on that day.")
#         return None, None

#     print("Available time slots (aggregated across devices):")
#     sorted_slots = sorted(available_slots.keys())
#     for idx, slot in enumerate(sorted_slots):
#         start_str = slot[0].strftime('%I:%M %p')
#         end_str = slot[1].strftime('%I:%M %p')
#         num_available = len(available_slots[slot])
#         print(f"{idx + 1}: {start_str} - {end_str} (Devices available: {num_available})")
    
#     try:
#         selection = int(input("Select a slot by number: "))
#         if selection < 1 or selection > len(sorted_slots):
#             print("Invalid selection.")
#             return None, None
#     except ValueError:
#         print("Invalid input. Please enter a number.")
#         return None, None

#     chosen_slot = sorted_slots[selection - 1]
#     # Automatically choose one device.
#     candidate = sorted(available_slots[chosen_slot])[0]
#     try:
#         chosen_device = int(candidate)
#     except ValueError:
#         chosen_device = candidate
#     return chosen_slot, chosen_device

# def interactive_reserve_all():
#     """
#     Interactive function that prompts for a reservation date,
#     displays aggregated free 1-hour slots (with an accurate count of available devices),
#     and reserves the chosen slot on one available device.
#     """
#     try:
#         date_input = input("Enter the date for reservation (YYYY-MM-DD): ")
#         reservation_date = datetime.datetime.strptime(date_input, '%Y-%m-%d').date()

#         chosen_slot, chosen_device = display_free_slots_all(reservation_date)
#         if chosen_slot is None:
#             return

#         token = account.reserve_device(chosen_device, chosen_slot[0], chosen_slot[1])
#         if token != '':
#             print(f"Reservation successful on device {chosen_device}. Thy Token -> {token}")
#             print("Please keep this token safe, as it is not saved on server side, and cannot be regenerated/reretrieved.")
#     except Exception as e:
#         print(f"Error: {e}")

# def display_free_slots_next_days(num_days: int):
#     """
#     Display available 1-hour slots aggregated across all devices for the next num_days (starting today).
#     A slot is available if at least one device is free (i.e. not reserved during that slot).
#     Omits any slots whose end time is in the past (for today).
#     Returns a tuple (chosen_day, chosen_slot, chosen_device) where:
#       - chosen_day is a datetime.date for the reservation day,
#       - chosen_slot is a tuple (start_time, end_time), and
#       - chosen_device is one available device for that slot.
#     If no slot is available, returns (None, None, None).
#     """
#     today = datetime.date.today()
#     devices = fetch_all_devices()
#     now = datetime.datetime.now()
    
#     # Compute the end day (inclusive)
#     end_day = today + datetime.timedelta(days=num_days - 1)
#     # Fetch all reservations for the entire range (one network call)
#     reservations_range = fetch_reservations_for_range(today, end_day)
    
#     available_slots = []  # List of tuples: (day, slot, free_devices)
    
#     for i in range(num_days):
#         day = today + datetime.timedelta(days=i)
#         all_slots = build_hourly_slots(day)
#         for slot in all_slots:
#             # If the day is today, skip slots that have already ended.
#             if day == today and slot[1] <= now:
#                 continue
#             free_devices = []
#             for dev in devices:
#                 # Look up reservations for this device on this day.
#                 key = (dev, day)
#                 current_res = reservations_range.get(key, [])
#                 if not is_slot_conflicting(slot, current_res):
#                     free_devices.append(dev)
#             if free_devices:
#                 available_slots.append((day, slot, free_devices))
    
#     if not available_slots:
#         print(f"No available time slots for any device in the next {num_days} days.")
#         return None, None, None

#     # Sort by day and slot start time.
#     available_slots.sort(key=lambda x: (x[0], x[1][0]))
    
#     print(f"Available time slots for the next {num_days} days:")
#     last_day = None
#     for idx, (day, slot, free_devices) in enumerate(available_slots):
#         # When a new day starts, print a header line with the date and formatted day.
#         if last_day is None or day != last_day:
#             # Format: YYYY-MM-DD (Abbreviated Weekday) AbbrevMonth. day
#             # Example: "2025-02-04 (Tue) Feb. 4"
#             day_header = f"{day.strftime('%Y-%m-%d')} ({day.strftime('%a')}) {day.strftime('%b')}. {day.day}"
#             print("\n" + day_header)
#             last_day = day
#         start_str = slot[0].strftime('%I:%M %p')
#         end_str = slot[1].strftime('%I:%M %p')
#         print(f"  {idx+1}: {start_str} - {end_str} (Devices available: {len(free_devices)})")
    
#     try:
#         selection = int(input("Select a slot by number: "))
#         if selection < 1 or selection > len(available_slots):
#             print("Invalid selection.")
#             return None, None, None
#     except ValueError:
#         print("Invalid input. Please enter a number.")
#         return None, None, None

#     chosen_day, chosen_slot, free_devices_for_slot = available_slots[selection - 1]
#     candidate = sorted(free_devices_for_slot)[0]
#     try:
#         chosen_device = int(candidate)
#     except ValueError:
#         chosen_device = candidate
#     return chosen_day, chosen_slot, chosen_device

# def interactive_reserve_next_days():
#     """
#     Interactive function that prompts the user for the number of days (starting today) to check for available reservations.
#     It displays aggregated free 1-hour slots over that period and reserves the chosen slot on one available device,
#     after confirming with the user.
#     """
#     try:
#         num_days = int(input("Enter the number of days to check for available reservations (starting today): "))
#         chosen_day, chosen_slot, chosen_device = display_free_slots_next_days(num_days)
#         if chosen_slot is None:
#             return

#         start_time = chosen_slot[0].strftime('%I:%M %p')
#         end_time = chosen_slot[1].strftime('%I:%M %p')
#         confirmation = input(f"You have selected a reservation on {chosen_day.strftime('%Y-%m-%d')} from {start_time} to {end_time} on device {chosen_device}. Confirm reservation? (y/n): ").strip().lower()
#         if confirmation != 'y':
#             print("Reservation cancelled.")
#             return

#         token = account.reserve_device(chosen_device, chosen_slot[0], chosen_slot[1])
#         if token != '':
#             print(f"Reservation successful on device {chosen_device} for {chosen_day.strftime('%Y-%m-%d')}. Thy Token -> {token}")
#             print("Please keep this token safe, as it is not saved on server side, and cannot be regenerated/reretrieved.")
#     except Exception as e:
#         print(f"Error: {e}")
