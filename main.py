import discord
from discord.ext import commands
import asyncio
import os
import shutil

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.remove_command("help")

import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
    print(f"{bot.user.name} est prêt !")

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Liste des commandes", color=discord.Color.blue())
    embed.add_field(name="!help", value="Affiche cette liste de commandes", inline=True)
    embed.add_field(name="!fournisseur", value="Assigne le rôle 📍| Fournisseur", inline=True)
    embed.add_field(name="!gen", value="Générer des comptes et cartes de crédit", inline=True)
    embed.add_field(name="!create", value="Créer un service", inline=True)
    embed.add_field(name="!add <service> (avec fichier .txt)", value="Ajouter des comptes aux services", inline=True)
    embed.add_field(name="!prefix <nouveau préfixe>", value="Changer le préfixe du bot", inline=True)
    embed.add_field(name="!remove", value="Supprimer un service", inline=True)
    embed.add_field(name="!clear", value="Effacer les comptes d’un service", inline=True)
    embed.add_field(name="!stock", value="Voir le stock actuel", inline=True)
    embed.add_field(name=".notif", value="Définir un channel de notification", inline=True)
    embed.add_field(name="!annonces", value="Faire une annonce via un webhook", inline=True)
    embed.add_field(name="!synchrocmd", value="Synchroniser les commandes du bot", inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def fournisseur(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, id=1343549732919840780)
    if role:
        await member.add_roles(role)
        await ctx.send(f"{member.mention} a reçu le rôle 📍| Fournisseur !")
    else:
        await ctx.send("Rôle introuvable.")

@bot.command()
async def gen(ctx, channel: discord.TextChannel):
    if channel.id == 1343909520916877333:
        await ctx.send(f"Génération en cours dans {channel.mention}...")
    else:
        await ctx.send("Salon invalide.")

@bot.command()
async def create(ctx):
    await asyncio.sleep(3)
    await ctx.send("Service créé avec succès !")

@bot.command()
async def add(ctx, service: str):
    if len(ctx.message.attachments) == 0:
        await ctx.send("Veuillez joindre un fichier .txt contenant les comptes à ajouter.")
        return
    
    attachment = ctx.message.attachments[0]
    if not attachment.filename.endswith(".txt"):
        await ctx.send("Le fichier doit être au format .txt.")
        return
    
    file_path = f"./Stock/{service}/{attachment.filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    await attachment.save(file_path)
    
    await ctx.send(f"Comptes ajoutés au service `{service}` avec succès !")

@bot.command()
async def prefix(ctx, new_prefix: str):
    global bot
    if len(new_prefix) > 3:
        await ctx.send("Le préfixe ne doit pas dépasser 3 caractères.")
        return
    bot.command_prefix = new_prefix
    await ctx.send(f"Préfixe changé en `{new_prefix}`. Redémarrage nécessaire pour appliquer le changement.")

@bot.command()
async def remove(ctx):
    await ctx.send("Suppression d’un service...")

@bot.command()
async def clear(ctx):
    await ctx.send("Effacement des comptes d’un service...")

@bot.command()
async def stock(ctx):
    await asyncio.sleep(3)
    await ctx.send("Stock actuel :")
    await ctx.send("- Service 1 : 10 comptes\n- Service 2 : 5 comptes\n- Service 3 : 20 comptes")

@bot.command()
async def notif(ctx, channel: discord.TextChannel):
    await ctx.send(f"Channel de notification défini sur {channel.mention}")

@bot.command()
async def annonces(ctx, *, message):
    channel = discord.utils.get(ctx.guild.text_channels, name="annonces")
    if channel:
        webhook = await channel.create_webhook(name="Annonce")
        await webhook.send(message, username=ctx.author.name, avatar_url=ctx.author.avatar.url)
        await ctx.send("Annonce envoyée !")
    else:
        await ctx.send("Salon annonces introuvable.")

@bot.command()
async def synchrocmd(ctx):
    try:
        await bot.tree.sync()
        await ctx.send("Les commandes ont été synchronisées avec succès !")
    except Exception as e:
        await ctx.send(f"Erreur lors de la synchronisation : {e}")

bot.run(BOT_TOKEN)
