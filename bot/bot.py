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
        if self.units.of_type(UnitTypeId.SCV).amount < Limit:
            CommandCenters: Units = self.townhalls.filter(lambda CC: CC.is_idle and CC.is_ready)
            if CommandCenters and self.can_afford(UnitTypeId.SCV):
                CommandCenter: Unit = CommandCenters.random
                CommandCenter.train(UnitTypeId.SCV)
                return True
            elif not self.townhalls.filter(lambda CommandCenter: CommandCenter.is_ready):
                return False
            return True
        return True
    async def Depots(self, Limit: int) -> bool:
        Total: int = self.structures.of_type({UnitTypeId.SUPPLYDEPOT, UnitTypeId.SUPPLYDEPOTLOWERED}).amount
        if Total < Limit and self.can_afford(UnitTypeId.SUPPLYDEPOT):
            if Limit <= 2:
                Placement = self.DepotPlacements.pop()
                SCV: Unit = self.workers.filter(lambda Worker: not Worker.is_returning).closest_to(Placement)
                if SCV:
                    SCV.build(UnitTypeId.SUPPLYDEPOT, Placement)
                    return True
                else:
                    return False
                #Worker: Unit = self.workers.filter(lambda x: not x.is_returning).closest_to(Position)
            else:
                return True
        return True

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

            # Variable Management:

            # Depots:
            self.DepotPlacements = self.main_base_ramp.corner_depots
            self.ExistingDepots: Units = self.structures.of_type({UnitTypeId.SUPPLYDEPOT, UnitTypeId.SUPPLYDEPOTLOWERED})

            if self.ExistingDepots:
                self.ExistingDepots = {SupplyDepot for SupplyDepot in self.DepotPlacements
                    if self.ExistingDepots.closest_distance_to(SupplyDepot) > 1}
            
            # Protocols:
            if self.Compare(self.Tactic, '3-1-1'):
                if self.Compare(self.Override, False):
                    print(f"Iteration: {iteration}")
            elif self.Compare(self.Tactic, '2-1-1'):
                if self.Compare(self.Override, False):
                    Sequence = Foundation([
                        self.SCVs(13),
                        self.Depots(1),
                        self.SCVs(14)
                    ])
                    await Sequence.Execute()
            elif self.Compare(self.Tactic, '1-1-1'):
                if self.Compare(self.Override, False):
                    print(f"Iteration: {iteration}")
