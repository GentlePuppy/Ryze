# Written by: Christopher Gholmieh
# For: Ryze

# Packages:
import random
import sc2

# Modules:

from sc2.ids.unit_typeid import UnitTypeId
from sc2.units import Units
from sc2.unit import Unit
from sc2.bot_ai import BotAI
from sc2.data import Race

# Classes:
class Foundation:
    def __init__(self, List: list):
        self.Actions: list = List
    
    async def Execute(self):
        for Action in self.Actions:
            Result = await Action
            if Action is False:
                break
            elif Action is True:
                continue

class CompetitiveBot(BotAI):
    
    # Initialization:
    def __init__(self):
        self.Override: bool = False
        self.Tactics: dict = {
            Race.Protoss: ['3-1-1'],
            Race.Terran: ['1-1-1'],
            Race.Zerg: ['2-1-1'],
        }

    RACE: Race = Race.Terran
    NAME: str = 'Ryze'

    # Functions:
    def Compare(self, Argument, Argument_):
        if Argument == Argument_:
            return True
        else:
            return False
    
    # Tactic Methods:
    async def SCVs(self, Limit: int) -> bool:
        CommandCenters: Units = self.townhalls.filter(lambda CC: CC.is_idle and CC.is_ready)
        if CommandCenters and self.can_afford(UnitTypeId.SCV):
            CommandCenter: Unit = CommandCenters.random
            if self.units.of_type(UnitTypeId.SCV).amount < Limit:
                CommandCenter.train(UnitTypeId.SCV)
                return True
            return True
        return False
    
    async def Depots(self, Limit: int):
        pass

    # Methods:
    async def on_start(self):
        # Variables:
        Library: list = self.Tactics[self.enemy_race]
        Integer: int = random.randint(1, len(Library))

        # Setup:
        self.Tactic: str = Library[Integer - 1]

        # Misc:
        await self.chat_send(f'Strategy: {self.Tactic}', True)

    async def on_step(self, iteration: int):
        if self.townhalls:

            # Protocols:
            if self.Compare(self.Tactic, '3-1-1'):
                if self.Compare(self.Override, False):
                    print(f"Iteration: {iteration}")
            elif self.Compare(self.Tactic, '2-1-1'):
                if self.Compare(self.Override, False):
                    Sequence = Foundation([
                        self.SCVs(13),
                        
                    ])
                    await Sequence.Execute()
            elif self.Compare(self.Tactic, '1-1-1'):
                if self.Compare(self.Override, False):
                    print(f"Iteration: {iteration}")
