from discord.ext import commands
from discord.ext.commands import Context

import random

class DuelTournament(commands.Cog, name="duel_tournament"):
    def __init__(self, bot):
        self.bot = bot

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

                # Duel the members and update their scores
                winner = self.duel(member1, member2)
                if winner == member1:
                    scores[member1] += 1
                elif winner == member2:
                    scores[member2] += 1

        # Determine the winner of the tournament
        winner = max(scores, key=scores.get)

        # Announce the winner
        await context.send(f"{winner.mention} is the winner of the tournament with {scores[winner]} wins!")

    def duel(self, member1, member2):
        """
        Duel two members and return the winner.

        :param member1: The first member to duel.
        :param member2: The second member to duel.
        :return: The member who won the duel.
        """
        # Determine the winner of the duel randomly
        return random.choice([member1, member2])

async def setup(bot):
    await bot.add_cog(DuelTournament(bot))