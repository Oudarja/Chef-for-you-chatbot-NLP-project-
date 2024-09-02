'''
A webhook in Dialogflow is a way to enable your Dialogflow agent
to communicate with external services or APIs in real-time. 
When a user interacts with your agent, Dialogflow can send a request
to your webhook, which processes the request and can return a response
back to the agent.
'''

# uvicorn main:app --reload

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db_helper 

import session_id_finder
import get_str_from_food_dict

import save_to_db_helper

app=FastAPI()


inprogress_orders={}


# Which is written in dialogflow will be posted here through fast api  
@app.post("/")
async def handle_request(request: Request):
    # retrieve the json data from the request
    payload=await request.json()

    # extract the necessary information from the payload
    # based on the structure of the WebhookRequest from Dialogflow

    intent=payload['queryResult']['intent']['displayName']
    parameters=payload['queryResult']['parameters']
    output_contexts=payload['queryResult']['outputContexts']
    
    session_id=session_id_finder.extract_session_id(output_contexts[0]['name'])



    if intent=="track.order-context:ongoing-tracking":
        return track_order(parameters,session_id)
    elif intent=="order.add-context:ongoing-order":
        return add_to_order(parameters,session_id)
    elif intent=="order.complete-context:ongoing-order":
        return complete_order(parameters,session_id)
    elif intent=="order.remove-context:ongoing-order":
        return remove_from_order(parameters,session_id)



def remove_from_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fullfillmentText": "I'm having trouble finding your order. Sorry! Can you place a new order?"
        })
    
    current_order = inprogress_orders[session_id]
    food_items = parameters["food-item"]
    number_to_be_removed = parameters["number"]

    removed_items = []
    no_such_items = []
    fulfillment_text = ""

    for item, number in zip(food_items, number_to_be_removed):
        if item not in current_order:
            no_such_items.append(item)
        elif current_order[item] < number:
            no_such_items.append(f"{item} (requested: {int(number)}, available: {current_order[item]})")
        else:
            removed_items.append((item, number))
            current_order[item] -= number
            if current_order[item] == 0:
                del current_order[item]  # Remove item if quantity is zero

    if removed_items:
        removed_str = ', '.join([f"{item} (removed: {int(number)})" for item, number in removed_items])
        fulfillment_text += f'Removed {removed_str} from your order. '
    
    if no_such_items:
        no_such_str = ', '.join(no_such_items)
        fulfillment_text += f'Your current order does not have {no_such_str}. '

    if not current_order:
        fulfillment_text += "Your order is empty!"
    else:
        order_str = get_str_from_food_dict.get_str_from_food_dict(current_order)
        fulfillment_text += f"Here is what is left in your order: {order_str}."

    # Update the global inprogress_orders dictionary
    inprogress_orders[session_id] = current_order

    del current_order

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })



        
def add_to_order(parameters:dict,session_id:str):
    food_items=parameters["food-item"]
    quantities=parameters["number"]

    if len(food_items)!=len(quantities):
        fulfillment_text="Sorry I didn't understand. Can you please specify food items and quantites?"
    else:

        new_food_dict=dict(zip(food_items,quantities))

        if session_id in inprogress_orders:
            current_food_dict=inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
        else:
            inprogress_orders[session_id]=new_food_dict

        order_str=get_str_from_food_dict.get_str_from_food_dict(inprogress_orders[session_id])

        fulfillment_text=f"So far you have : {order_str}. Do you need anything else?"
    

    return JSONResponse(content={

        "fulfillmentText": fulfillment_text
    })
    



def complete_order(parameters:dict,session_id:str):
    if session_id not in inprogress_orders:
        fulfillment_text="I'm having a trouble finding your order. Sorry! can you place a new order?"

    else:
        order=inprogress_orders[session_id]
        order_id,order_total=save_to_db_helper.save_to_db(order)

        if order_id==-1:
            fulfillment_text="Sorry, I could not process your order due to a backend error.Please place a new order agian"
        else:
            # order_total=db_helper.get_total_order_price(order_id)

            # This is a text fullfillment_text is an example of an f-string
            # f"": This indicates that the string is an f-string, allowing 
            # you to embed expressions inside curly braces {}. The values of 
            # these expressions will be evaluated at runtime and formatted into the string. 

            # The backslash is used to escape characters in Python strings. 



            fulfillment_text=f"Awesome! We have placed your order."\
                              f"Your order id : {order_id}."\
                              f"Your order total price is : {order_total}."
            

        del inprogress_orders[session_id]
        

        
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })
                
                             

    
    





def track_order(parameters: dict,session_id:str):

    order_id=int(parameters['number'])

    order_status=db_helper.get_order_status(order_id)

    if order_status:
        fulfillment_text=f"The order status for order id: {order_id} is: {order_status}"
    else:
        fulfillment_text=f"No order found with order id:{order_id}"

    return JSONResponse(content={
        "fulfillmentText":fulfillment_text
    })
