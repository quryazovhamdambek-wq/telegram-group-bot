import asyncio
import os
import threading
from flask import Flask
from telethon import TelegramClient, errors
from telethon.tl.functions.channels import InviteToChannelRequest

# ===== SOZLAMALAR (Render Environment Variables dan o'qiydi) =====
API_ID = int(os.environ.get('API_ID', 1234567))
API_HASH = os.environ.get('API_HASH', 'your_api_hash')
PHONE = os.environ.get('PHONE', '+998901234567')

MANBA_KANAL = os.environ.get('MANBA_KANAL', '@beminnatvakant_ish')
MAQSAD_KANAL = os.environ.get('MAQSAD_KANAL', '@sizning_kanalingiz')

QOSHISH_SONI = os.environ.get('QOSHISH_SONI', None)  # None -> hammasi
if QOSHISH_SONI:
    QOSHISH_SONI = int(QOSHISH_SONI)

KUTISH_SONIYA = int(os.environ.get('KUTISH_SONIYA', 5))
# ================================================================

app = Flask(__name__)

@app.route('/')
@app.route('/health')
def health():
    return "Bot is running", 200

async def main():
    client = TelegramClient('session', API_ID, API_HASH)
    await client.start(phone=PHONE)
    print("✅ Bot ishga tushdi!")

    manba = await client.get_entity(MANBA_KANAL)
    maqsad = await client.get_entity(MAQSAD_KANAL)

    print("📥 Obunachilar ro'yxati olinmoqda...")
    users = []
    async for user in client.iter_participants(manba):
        users.append(user)
        if QOSHISH_SONI and len(users) >= QOSHISH_SONI:
            break

    print(f"👥 {len(users)} ta odam topildi")

    qoshildi = 0
    for user in users:
        try:
            await client(InviteToChannelRequest(maqsad, [user.id]))
            qoshildi += 1
            print(f"✅ {qoshildi}. {user.first_name} qo'shildi")
        except errors.FloodWaitError as e:
            print(f"⏳ Bloklandi, {e.seconds} soniya kutish kerak")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"❌ {user.first_name} qo'shilmadi: {e}")

        await asyncio.sleep(KUTISH_SONIYA)

    print(f"🎉 Yakunlandi! {qoshildi} ta odam qo'shildi.")
    await client.disconnect()


def run_userbot():
    asyncio.run(main())


if __name__ == '__main__':
    threading.Thread(target=run_userbot).start()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
