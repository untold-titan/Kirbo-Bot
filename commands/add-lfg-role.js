const { ActionRowBuilder, StringSelectMenuBuilder } = require('@discordjs/builders');
const { SlashCommandBuilder } = require('discord.js');
const {roles} = require("../roles.json");

module.exports = {
	data: new SlashCommandBuilder()
		.setName('add_lfg_role')
		.setDescription('Adds an LFG Role to the user'),
	async execute(interaction) {
        const roleSelect = new ActionRowBuilder()
        .addComponents(
            new StringSelectMenuBuilder()
            .setCustomId("role_select")
            .setPlaceholder("Pick a role!")
            .setMinValues(1)
            .setMaxValues(100)
            .addOptions(roles)
        )
		await interaction.reply({content:"Please pick a role!", components:[roleSelect]});
	},
};