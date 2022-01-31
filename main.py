from ast import Return
from multiprocessing.connection import Client
import os.path
import nextcord 
from nextcord.ext import commands
from nextcord.utils import get
from nextcord.ext import menus

#bot start-up
intents = nextcord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix=".",intents=intents)

#on-ready
@client.event
async def on_ready():
    for guild in client.guilds:
    	print(f'{client.user} is connected to the following guild:\n'
          f'{guild.name}(id: {guild.id})')
#perms = json.load(open("perms.json", "a+"))

# setup
@client.command(name = 'setup', help= 'sets up bot and blacklist channels')
async def make_chan(ctx):
  user = ctx.message.author
  

  if ctx.guild.owner_id != user.id:
    await ctx.send('you are not the owner')
  
  else:
    await ctx.send('Starting setup please wait......')
    Chan_name = []
    for channel in ctx.guild.text_channels:
      if str(channel.type) == 'text':

        Chan_name.append(channel.name)
        
        await ctx.send('Creating beepu_logs')
        if "beepu_logs" not in Chan_name:
            await ctx.message.guild.create_text_channel("beepu_logs")
        else:
            await ctx.send('Blacklist logs already created ')

        await ctx.send('Creating mod_logs')
        if "mod_logs" not in Chan_name:
            await ctx.message.guild.create_text_channel("mod_logs")
        else:
            await ctx.send('Broadcast alerts already created')
        

        await ctx.send('Setup finished')
        
        return


'''@client.command(name = 'add_admin', help = 'adds one of your admin roles to unlock commands')
async def add(ctx, role):
    user = ctx.message.author
    owner = ctx.guild.owner()
    if user != owner:
       await ctx.send('you are not the owner')'''

     
    


@client.command(name = 'ban', help = 'bans a member')
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : nextcord.Member, *, reason = None):
    auth =ctx.message.author
    #await ctx.guild.ban( member, reason = reason )
    await ctx.send(f'{member} has been banned')
    channel = nextcord.utils.get(ctx.guild.channels, name="mod_logs")
    ban_msg = (f"{member} was banned for {reason} by {auth}")
    embed=nextcord.Embed(title="Beepu Moderation", description= f"{member} was banned for {reason} by {auth}", color=0xF0FFFF)
    await ctx.channel.send(embed=embed)

# unban
@client.command(name ='unban', help = 'unbans a member ')
@commands.has_permissions(administrator = True)
async def unban(ctx, member : nextcord.member ):
    auth =ctx.message.author
    banned_users = await ctx.guild.bans()
    #user, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name + user.discriminator) == (member):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            channel= nextcord.utils.get(ctx.guild.channels, name="mod_logs")
            unban_mgs = f'{user.mention} has been unbanned by {auth}'
            embed=nextcord.Embed(title="Beepu Moderation", description= unban_mgs, color=0xF0FFFF)
            await ctx.channel.send(embed=embed)
  
            return

# kick command 
@client.command(name = 'kick' , help = 'kicks a member')
async def kick(ctx, member : nextcord.Member, *, reason = None ):
    auth =ctx.message.author
    await ctx.member.kick(reason = reason)
    await ctx.send(f'{member} has been kicked')
    channel = nextcord.utils.get(ctx.guild.channels, name="mod_logs")
    ban_msg = (f"{member} was kicked for {reason} by {auth}")
    embed=nextcord.Embed(title="Beepu Moderation", description= f"{member} was banned for {reason} by {auth}", color=0xF0FFFF)
    await ctx.channel.send(embed=embed)

#lock command 




#purge command




#stats command 



#user info command 


#on_ban logs
@client.event
async def on_member_ban(guild,user):
    channel = nextcord.utils.get(guild.channels, name="beepu_logs")
    embed=nextcord.Embed(title="Beepu Moderation logs", description= f"{user} was banned", color=0xF0FFFF)
    await channel.send(embed=embed)

with open('token.txt') as f:
    TOKEN = f.read()


client.run(TOKEN)

