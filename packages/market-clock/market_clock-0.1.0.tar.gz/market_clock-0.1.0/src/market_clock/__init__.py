import datetime
import time
from itertools import cycle

from blessed import Terminal

from market_clock.get_market_info import ALL_MARKET_INFO


def get_next_trading_day(start_date, holidays, trading_weekdays):
    next_day = start_date + datetime.timedelta(days=1)
    while True:
        if next_day.weekday() in trading_weekdays and next_day not in holidays:
            return next_day
        next_day += datetime.timedelta(days=1)


def format_timedelta(delta):
    total_seconds = int(delta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def get_market_status(market_name, market_info):
    timezone = market_info["timezone"]
    trading_weekdays = market_info["trading_weekdays"]
    holidays = market_info["holidays"]
    half_days = market_info["half_days"]
    start_time = market_info["start_time"]
    end_time = market_info["end_time"]
    half_day_end_time = market_info["half_day_end_time"]
    is_have_lunch_break = market_info["is_have_lunch_break"]
    if is_have_lunch_break:
        lunch_break_start = market_info["lunch_break_start"]
        lunch_break_end = market_info["lunch_break_end"]

    local_time = datetime.datetime.now(timezone)
    current_time = local_time.time()
    current_date = local_time.date()

    if current_date > max(holidays | half_days):
        msg = f"{market_name} holiday list is not up-to-date."
        raise ValueError(msg)
    if holidays & half_days:
        msg = f"{market_name} has overlapping holidays/half-days"
        raise ValueError(msg)

    if current_date in holidays or local_time.weekday() not in trading_weekdays:
        is_open = False
    elif current_date in half_days:
        is_open = start_time <= current_time <= half_day_end_time
    elif is_have_lunch_break:
        is_open = (start_time <= current_time < lunch_break_start) or (
            lunch_break_end < current_time <= end_time
        )
    else:
        is_open = start_time <= current_time <= end_time

    if is_open:

        # No lunch break or pass lunch break, next event is close
        if not is_have_lunch_break or current_time > lunch_break_end:
            event_time = timezone.localize(
                datetime.datetime.combine(current_date, end_time)
            )
        # has lunch break, is currently before lunch break, next event is lunch break
        elif is_have_lunch_break and current_time < lunch_break_start:
            event_time = timezone.localize(
                datetime.datetime.combine(current_date, lunch_break_start)
            )
        else:
            raise ValueError("Should not be possible.")

    else:

        # This is trading day, and the session has not ended
        if local_time.weekday() in trading_weekdays and current_date not in holidays and current_time < end_time:
            
            # session not sratrted, next event is start
            if current_time < start_time:
                event_time = timezone.localize(
                    datetime.datetime.combine(current_date, start_time)
                )

            # session sratrted, in the middle of lunch break,  next event is lunch break end
            elif is_have_lunch_break and lunch_break_start <= current_time <= lunch_break_end:
                event_time = timezone.localize(
                    datetime.datetime.combine(current_date, lunch_break_end)
                )

            else:
                raise ValueError("Should not be possible.")

        # Not a trading day, or the trading session has already ended. Next event is the next trading day.
        else:
            next_day = get_next_trading_day(current_date, holidays, trading_weekdays)
            event_time = timezone.localize(
                datetime.datetime.combine(next_day, start_time)
            )

    return is_open, event_time


def main():
    term = Terminal()
    spinner = cycle("🕛🕧🕐🕜🕑🕝🕒🕞🕓🕟🕔🕠🕕🕡🕖🕢🕗🕣🕘🕤🕙🕥🕚🕦")

    longest_market_name_length = max(len(k) for k in ALL_MARKET_INFO)

    with term.fullscreen(), term.hidden_cursor():
        try:
            while True:
                spinner_char = next(spinner)

                clock_lines = []

                for market in ALL_MARKET_INFO:
                    is_open, event = get_market_status(market, ALL_MARKET_INFO[market])

                    clock_line = (
                        f"{market.rjust(longest_market_name_length)} "
                        f"{'OPEN 🟢' if is_open else 'CLOSED 🟠'} | "
                        f"{'Closes' if is_open else 'Opens'} in "
                        f"{format_timedelta(event - datetime.datetime.now(ALL_MARKET_INFO[market]['timezone']))} "
                        f"{spinner_char}"
                    )

                    clock_lines.append(clock_line)

                clock_lines = "\n".join(clock_lines)

                clock = term.move(0, 0) + term.clear_eos + clock_lines

                # Update display
                print(clock)
                time.sleep(1)

        except KeyboardInterrupt:
            print(term.move_down(2) + "Countdown stopped.")


if __name__ == "__main__":
    main()
