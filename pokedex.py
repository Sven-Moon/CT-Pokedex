import requests as r
import json

class Pokemon:
    def __init__(self, name, abilities, weight, types) -> None:
        self.name = name
        self.abilities = abilities
        self.weight = weight
        self.types = types
        
    def describe(self):
        print('Name:', self.name)
        print('Abilities: ', end = "")
        print(", ".join(self.abilities))
        print("Weight:", self.weight)
        print("Types: ", end="")
        print(", ".join(self.types))
        
    def desc_as_dict(self):
        return self.__dict__
    
    def report_name(self):
        print('Name:', self.name)
    
    def get_types(self):
        return self.types
        

class Pokedex:
    def __init__(self):
        self.data = {}
        self.byType = {}
        
    def addPokemon(self, pokemon):
        self.data[pokemon.name] = pokemon
        
    def listAll(self):
        for name, info in self.data.items():
            print(f'{name}'.title(), f"({', '.join(info.get_types())})")
            # print(f'{name} - {", ".join(info["types"])}'.title())
            
    def search(self, name):
        self.data[name.lower()].describe()
            
            
    def getAllPokemon(self):
        data = r.get('https://pokeapi.co/api/v2/pokemon')
        if data.status_code == 200:
            names = data.json()
        else:
            print('Problem getting names')
        all_names = [d['name'] for d in names["results"]]
        for name in all_names:
            data = r.get(f'https://pokeapi.co/api/v2/pokemon/{name}')  
            if data.status_code == 200:
                pokemon = data.json()
                abilities = [ability['ability']['name'] for ability in pokemon['abilities']]
                weight = pokemon['weight']
                types = [t['type']['name'] for t in pokemon['types']]
                
                newPokemon = Pokemon(name, abilities, weight, types)                
                self.addPokemon(newPokemon)
        # with open('pokemon.txt', 'w') as file:
        #     file.write(json.dumps(self.data))
            
    def listByType(self):
        # for each poke 
        for pokemon in self.data.values():
            # loop through types
            for this_type in pokemon.get_types():
                # set the value to a dict item, as a dictionary, appending the name                
                self.byType.setdefault(this_type, []).append(pokemon.name)
        for k, v in self.byType.items():
            print(f"{k}:".title(), f"{', '.join(v)}".title())
        
            

def main():
    mydex = Pokedex()
    mydex.getAllPokemon()
    print(' List of All '.center(20, "-"))
    mydex.listAll()
    print('')
    print(' List by type '.center(20, "-"))
    mydex.listByType()
    print('')
    print(mydex.search('Weedle'))
    
main()