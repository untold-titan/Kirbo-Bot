const { SlashCommandBuilder } = require('discord.js');
require("dotenv").config(); // Setup process.env

module.exports = {
	data: new SlashCommandBuilder()
		.setName('about')
		.setDescription('Replies with information about the bot'),
	async execute(interaction) {
		const embed = {
			title:'Kirbo - JS - ' + process.env.VERSION_TYPE + ' - ' +  process.env.VERSION_NUMBER,
			description:"This version of Kirbo was developed with JavaScript",
			author:{
				name:"untold-titan",
				icon_url:"https://untoldtitan.netlify.app/titan.png",
				url:"https://www.github.com/untold-titan"
			}
		}
		await interaction.reply({embeds:[embed]});
	},
};