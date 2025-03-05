import time
import sys


def landing_simulation():
    # Boshlanish xabari
    print("Landing in progress...")

    # Progress bar uzunligi
    total_steps = 50

    for i in range(total_steps + 1):
        # Progres foizini hisoblash
        percent_complete = (i / total_steps) * 100

        # Progres bar
        bar = ('#' * i) + ('-' * (total_steps - i))

        # Bir qatorda progress bar va foizni chiqarish
        sys.stdout.write(f"\r[{bar}] {percent_complete:.2f}% Complete")
        sys.stdout.flush()  # Ekranga yozishni majburiy ravishda ko'rsatadi
        time.sleep(0.1)  # Progressni sekinlashtirish uchun 0.1 soniya kutadi
    print("\nLanding completed successfully!\n")
