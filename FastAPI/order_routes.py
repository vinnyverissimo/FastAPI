from fastapi import APIRouter, Depends, HTTPException
from models import Itens, Order, User
from schemas import OrderSchema, OrderItensSchema
from dependencies import create_session, checkToken

order_router = APIRouter(
    prefix="/orders", tags=["orders"], dependencies=[Depends(checkToken)])


@order_router.get("/")
async def get_orders():
    """
    Simulate fetching a list of orders. In a real application, you would retrieve this data from a database.
    """
    return {"message": "List of orders"}


@order_router.post("/create")
async def create_order(orderSchema: OrderSchema, session=Depends(create_session), user: User = Depends(checkToken)):
    newOrder = Order(user_id=user.id,
                     product_name=orderSchema.product_name, quantity=orderSchema.quantity)
    session.add(newOrder)
    session.commit()
    return {"message": "Order created successfully", "order": newOrder.id}


@order_router.get("/list")
async def list_orders(session=Depends(create_session), user: User = Depends(checkToken)):
    if not user.admin:
        raise HTTPException(
            status_code=403, detail="Only admin users can list all orders")
    else:
        orders = session.query(Order).all()
        return {"orders": orders}


@order_router.get("/{order_id}")
async def get_order(order_id: int, session=Depends(create_session)):
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        return {"message": "Order not found"}
    return {"order_id": order.id, "user_id": order.user_id, "product_name": order.product_name, "quantity": order.quantity, "status": order.status}


@order_router.post("/cancel/{order_id}")
async def cancel_order(order_id: int, session=Depends(create_session), user: User = Depends(checkToken)):
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not user.admin and user.id != order.user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to cancel this order")
    order.status = "cancelled"
    session.commit()
    return {"message": f"Order: {order.id} has been cancelled",
            "order": order}


@order_router.post("/add-item/{order_id}")
async def add_item(order_id: int, itemSchema: OrderItensSchema, session=Depends(create_session), user: User = Depends(checkToken)):
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not user.admin and user.id != order.user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to modify this order")
    newItem = Itens(order_id=order.id, flavor=itemSchema.flavor, size=itemSchema.size,
                    quantity=itemSchema.quantity, unit_price=itemSchema.unit_price)
    session.add(newItem)
    order.sumPrice()
    session.commit()
    return {"message": f"Item added to Order: {order.id}",
            "item": newItem.id,
            "OrderPrice": order.total_price}


@order_router.post("/remove-item/{item_id}")
async def remove_item(item_id: int, session=Depends(create_session), user: User = Depends(checkToken)):
    item = session.query(Itens).filter(Itens.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    order = session.query(Order).filter(Order.id == item.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not user.admin and user.id != order.user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to modify this order")
    session.delete(item)
    order.sumPrice()
    session.commit()
    return {"message": f"Item {item.id} removed from Order: {order.id}",
            "quantity": len(order.Itens),
            "Order": order}
