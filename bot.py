import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIGURAÇÕES ---
BOT_TOKEN = "8398411787:AAFdnFHGrwFoEz0hNa7Qo2sLRKQMrXMUACo"
PIX_CHAVE = "joaozinbrawl6@gmail.com"

GRUPOS = {
    "variedades": {
        "nome": "ZK HOT CLUB 🔥 Variedades",
        "link": "https://t.me/+2oqbp-UdEKg0YzEx"
    },
    "gold": {
        "nome": "ZK HOT CLUB 💎 Exclusivo Gold",
        "link": "https://t.me/+TF8V8GQIk8MxZDAx"
    },
    "diamond": {
        "nome": "ZK HOT CLUB 👑 Exclusivo Diamond",
        "link": "https://t.me/+OvtNc2CTAhQ0Yzk5"
    }
}

ADMINS = [5524093272]  # Seu ID como admin

# --- LOG ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

usuarios_pendentes = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Bem-vindo ao ZK HOT CLUB!

Digite /vip para ver os planos disponíveis."
    )

async def vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(GRUPOS["variedades"]["nome"], callback_data="variedades")],
        [InlineKeyboardButton(GRUPOS["gold"]["nome"], callback_data="gold")],
        [InlineKeyboardButton(GRUPOS["diamond"]["nome"], callback_data="diamond")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Escolha seu acesso VIP:", reply_markup=reply_markup)

async def escolha_plano(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    plano = query.data
    usuario = query.from_user

    usuarios_pendentes[usuario.id] = plano

    msg_pagamento = (
        f"💳 Para acessar **{GRUPOS[plano]['nome']}**, pague via PIX:
"
        f"🔑 Chave: `{PIX_CHAVE}`
"
        f"💰 Valor: Definido por você

"
        f"Após pagar, envie /confirmar."
    )

    await query.message.reply_text(msg_pagamento, parse_mode="Markdown")

async def confirmar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuario = update.message.from_user
    if usuario.id not in usuarios_pendentes:
        await update.message.reply_text("❌ Você não tem nenhum pagamento pendente.")
        return

    plano = usuarios_pendentes[usuario.id]
    for admin_id in ADMINS:
        await context.bot.send_message(
            chat_id=admin_id,
            text=f"⚠️ Pedido de acesso:
Usuário: @{usuario.username} ({usuario.id})
Plano: {GRUPOS[plano]['nome']}
Aprove com /aprovar {usuario.id}"
        )

    await update.message.reply_text("✅ Seu pedido foi enviado para aprovação. Aguarde...")

async def aprovar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id not in ADMINS:
        await update.message.reply_text("❌ Você não é admin.")
        return

    try:
        user_id = int(context.args[0])
    except:
        await update.message.reply_text("Uso correto: /aprovar <id_usuario>")
        return

    if user_id not in usuarios_pendentes:
        await update.message.reply_text("❌ Esse usuário não está pendente.")
        return

    plano = usuarios_pendentes.pop(user_id)
    link = GRUPOS[plano]["link"]

    await context.bot.send_message(
        chat_id=user_id,
        text=f"🎉 Aprovado! Aqui está seu link de acesso:
{link}"
    )

    await update.message.reply_text(f"✅ Acesso liberado para {user_id} no grupo {GRUPOS[plano]['nome']}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("vip", vip))
    app.add_handler(CallbackQueryHandler(escolha_plano))
    app.add_handler(CommandHandler("confirmar", confirmar))
    app.add_handler(CommandHandler("aprovar", aprovar))

    app.run_polling()

if __name__ == "__main__":
    main()
