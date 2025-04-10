from booking.booking import Booking
import time

with Booking() as bot:
    bot.land_first_page()
    bot.remove_popup()
    bot.change_currency("USD")
    bot.select_place("Dhaka")
    bot.select_datas(check_in_data='2025-04-10', check_out_date='2025-04-15')
    bot.select_adults(10)
    bot.search_booking()
    bot.filter_booking()
    bot.booking_report()
    time.sleep(20)
