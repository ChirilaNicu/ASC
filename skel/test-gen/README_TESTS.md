

## Testing system and theme tests

The test infrastructure can be used to generate test files in JSON format:

`` python test_generator h``

## Description of the contents of the input file:

### Marketplace Key (“marketplace”):

Object containing a single field, represented by a mapping between a string "queue_size" and an int, this representing the maximum size of the queue in which the manufacturer can write. 

**Exemplu**:
```json
    “marketplace”: {
        “queue_size”: 8
    }
```

### Products Key (“products”):
There will be several objects that will constitute the products that can be bought by customers. Each of these objects will be represented by a mapping between an “id” string and a product description. The description of the product concerned will consist of its specific elements, depending on the type of product made available. Following the resolution of this description, for each mapping a Product type object will be obtained which will enter the list of products that the Marketplace will make available to its customers. 


**Exemplu**: 
	Produsul ``Coffee(name=”Arabica”, price=10, acidity=5.1, roast_level=medium)`` va fi descris prin intermediul următoarei configurări:
```json
    “id1”: {
	    “prod_type”: “Coffee”,
	    “name”: “Arabica”,
	    “price”: 10,
	    “acidity”: 5.1,
	    “roast_level”: “medium”
    }
```


### Producer Key (“producers”):

Lista de obiecte -- fiecare obiect va contine următoarele mapări:


- “name”: numele producatorului
- “products”: lista de liste -- fiecare lista interioară va contine:
    - id-ul produsului pe care îl va furniza
    - cantitatea de produse de tipul respectiv furnizată
    - timpul de așteptare pentru producerea fiecărui produs
- “sleep_on_publish_false”: timpul de așteptare al producătorului în cazul în care acestuia nu îi mai este permisă furnizarea altor produse

**Exemplu**:
```json
	{
	    “name”: “prod1”,
		“products”: [
	        [“id1”, 2, 0.1],
	        [“id2”, 1, 0.3]
        ],
        “republish_wait_time”: 0.2
    }
```

The example above describes a single manufacturer named "prod1". The products it will provide have the ids id1, respectively id2 (ids that will be mapped to Coffee / Tea objects). The quantity of products that have the id “id1” with which the manufacturer will supply the “prod1” Marketplace, is 2, for those with the id “id2” being 1. Each product will have its own processing time: 
- produs “id1” -> 0.1 secunde
- produs “id2” -> 0.3 secunde


### Consumers Key (“consumers”):

Object list - each object contains the following mappings: 


- “name”: numele cumparatorului
- “retry_wait_time”: timpul de așteptare al consumatorului în cazul în care produsul pe care îl dorește nu este disponibil
- “carts”: lista de liste -- fiecare dintre listele interne va conține tipul de operație ce va fie efectuată de către consumator:
- “type” -- tipul operației
- “prod” -- id-ul produsului
- “quantity” -- cantitatea produsului

**Exemplu**:
```json
	{
		“name”: “cons1”,
		“sleep_on_add_false”: 0.1,
		“carts”: [
		    [
                { 
                    “type”: “add”,
                    “prod”: “id1”,
                    “quantity”: 2
                },
                {
			        “type”: “remove”,
			        “prod”: “id1”,
			        “quantity”: “1”
                }
            ],
			[
                {
                    “type”: “add”,
                    “prod”: “id2”,
                    “quantity”: 3
                }
             ],
    }
```

The example above describes a single consumer named "cons1". The operations that he will perform on his shopping cart are the following:

- will add to the cart two products with the id “id1”
- will remove from the cart a product with the id "id1"
- will add to the cart three products with the id “id2” 
