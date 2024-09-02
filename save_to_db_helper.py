import db_helper

def save_to_db(order:dict):


    next_order_id=db_helper.get_next_order_id()

    # order={"pizza":2,"chole":1}
    for food_item,quantity in order.items():

        return_code=db_helper.insert_order_item(
        food_item,
        quantity,
        next_order_id
        )

        if return_code==-1:
            return -1
    
    db_helper.insert_order_tracking(next_order_id,"in progress")
    order_total=db_helper.get_total_order_price(next_order_id)

        
    return next_order_id,order_total


