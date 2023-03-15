const fs = require('node:fs');
const path = require('node:path');
const { Client, GatewayIntentBits, Collection } = require('discord.js');
const client = new Client({ intents: [GatewayIntentBits.Guilds] });
require("dotenv").config(); // Setup process.env

client.commands = new Collection();

const commandsPath = path.join(__dirname, 'commands');
const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
	const filePath = path.join(commandsPath, file);
	const command = require(filePath);
	// Set a new item in the Collection with the key as the command name and the value as the exported module
	if ('data' in command && 'execute' in command) {
		client.commands.set(command.data.name, command);
	} else {
		console.log(`[WARNING] The command at ${filePath} is missing a required "data" or "execute" property.`);
	}
}


client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

//Handles select menus
client.on("interactionCreate", async interaction =>{
	if (!interaction.isStringSelectMenu()) return;
	if(interaction.customId == "role_select"){
		await interaction.update({content:"Gave you the role!",components:[]})
		interaction.values.forEach(value => {
			interaction.member.roles.add(value);
		})
	}
})

//Handles commands
client.on('interactionCreate', async interaction => {
	if (interaction.isStringSelectMenu()) return;
    if (!interaction.isChatInputCommand()) return;


    const command = interaction.client.commands.get(interaction.commandName);

	if (!command) {
		console.error(`No command matching ${interaction.commandName} was found.`);
		return;
	}

	try {
		await command.execute(interaction);
	} catch (error) {
		console.error(error);
		if (interaction.replied || interaction.deferred) {
			await interaction.followUp({ content: 'There was an error while executing this command!', ephemeral: true });
		} else {
			await interaction.reply({ content: 'There was an error while executing this command!', ephemeral: true });
		}
	}
});


client.login(process.env.TOKEN);