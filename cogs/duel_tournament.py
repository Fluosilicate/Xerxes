from discord.ext import commands
from discord.ext.commands import Context

import random
import asyncio

class DuelTournament(commands.Cog, name="tournament"):
    def __init__(self, bot):
        self.bot = bot
        self.duel_results = {}  # dictionary to store the results of each duel

    @commands.command(
        name="start_tournament",
        description="Starts a 1v1 duel tournament in the current voice channel.",
    )
    async def start_tournament(self, context: Context):
        """
        Starts a 1v1 duel tournament in the current voice channel.

        :param context: The application command context.
        """
        # Get the voice channel that the command was used in
        voice_channel = context.author.voice.channel
        if voice_channel is None:
            await context.send("You must be in a voice channel to use this command.")
            return

        # Get the members in the voice channel
        members = voice_channel.members
        if len(members) < 2:
            await context.send("There must be at least 2 members in the voice channel to start a tournament.")
            return

        # Shuffle the members to randomize the pairings
        random.shuffle(members)

        # Create a dictionary to store the scores for each member
        scores = {member: 0 for member in members}

        # Duel each member against every other member
        for i, member1 in enumerate(members):
            for j, member2 in enumerate(members):
                if i == j:
                    continue

                # Duel the members
                winner = await self.duel(context, member1, member2)

                # Update the scores based on the result of the duel
                if winner == member1:
                    scores[member1] += 1
                elif winner == member2:
                    scores[member2] += 1

                # Store the result of the duel in the duel_results dictionary
                self.duel_results[f"{member1.name} vs {member2.name}"] = winner.name

        # Determine the winner of the tournament
        winner = max(scores, key=scores.get)

        # Announce the winner
        await context.send(f"{winner} is the winner of the tournament with {scores[winner]} wins!")

    async def duel(self, context, member1, member2):
        """
        Duel two members and return the winner.

        :param context: The application command context.
        :param member1: The first member to duel.
        :param member2: The second member to duel.
        :return: The member who won the duel.
        """
        # Announce the start of the duel
        await context.send(f"{member1.mention}, {member2.mention}: it's time for your duel! The first to type 'I lost' loses the duel.")

        # Create a dictionary to store the responses from each member
        responses = {member1: None, member2: None}

        # Wait for both members to respond
        while None in responses.values():
            # Wait for a response from one of the members
            response = await self.bot.wait_for('message', check=lambda message: message.author in [member1, member2] and message.content.lower() == "i lost")

            # Store the response in the responses dictionary
            responses[response.author] = response.content

        # Determine the winner of the duel
        winner = next(member for member, response in responses.items() if response is not None)

        # Announce the winner of the duel
        await context.send(f"{winner.mention} wins the duel!")

        return winner

async def setup(bot):
    await bot.add_cog(DuelTournament(bot))