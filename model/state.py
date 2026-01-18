from dataclasses import dataclass

@dataclass
class State:
    id : str
    name : str
    capital: str
    lat : float
    lng : float
    area : int
    population : int
    neighbors : str


    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.name < other.name

    def __str__(self):
        return f"id: {self.id} | nome: {self.name} | capitale: {self.capital}"

    def __hash__(self):
        return hash(self.id)