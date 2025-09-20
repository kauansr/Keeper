from fastapi import APIRouter, Depends, HTTPException
from schemas.product import ProductResponse, ProductCreate, ProductUpdate
from services.product_service import ProductService
from api.v1.dependencies import get_db, get_current_user
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

product_route = APIRouter()


def get_product_service(db: Session = Depends(get_db)):
    """
    get the product services

    This function returns all product services from services.
    """
    return ProductService(db)


@product_route.get("/product", response_model=list[ProductResponse])
async def get_products(product_service: ProductService = Depends(get_product_service)):
    """
    List all product.

    This endpoint retrieves a list of all product from the system.

    Parameters:
    - product_service (ProductService): Dependency that provides the product service instance used to fetch product.

    Responses:
    - 200 OK: A list of product in the `ProductResponse` format.
    - 400 Bad Request: If no product are found, a `400` status is returned with the message "Any product!".

    Example usage:
    - Request: GET /product
    - Response: List of products or 400 if no products exist.
    """
    products = product_service.list_product()
    if not products:
        HTTPException(status_code=400, detail="Any Product!")
    return products


@product_route.post("/product", response_model=ProductResponse)
async def create_product(
    body: ProductCreate, product_service: ProductService = Depends(get_product_service)
):
    """
    Create a new product.

    This endpoint creates a new product in the system using the provided data.

    Parameters:
    - body (ProductCreate): The request body containing the information for creating a new product.
    - product_service (ProductService): Dependency that provides the product service instance to handle product creation.

    Responses:
    - 201 Created: The newly created product in the `ProductResponse` format.
    - 400 Bad Request: If the product creation fails due to invalid credentials, a `400` status is returned with the message "Invalid credentials!".

    Example usage:
    - Request: POST /product with product data in the body.
    - Response: Newly created product or 400 if invalid credentials are provided.
    """
    product_created = product_service.create_product(body)
    if not product_created:
        HTTPException(status_code=400, detail="Invalid credentials!")
    return product_created


@product_route.put("/product/update/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    product_service: ProductService = Depends(get_product_service),
):
    """
    Update an existing product.

    This endpoint updates an existing product's data based on the provided product ID and new product data.

    Parameters:
    - product_id (int): The ID of the product to be updated.
    - product_data (ProductUpdate): The new data for the product.
    - product_service (ProductService): Dependency that provides the productservice instance used to update the product.

    Responses:
    - 200 OK: The updated product information in the `ProductResponse` format.
    - 400 Bad Request: If the update operation fails, a `400` status is returned with the message "Update error!".

    Example usage:
    - Request: PUT /product/update/{product_id} with updated product data.
    - Response: Updated product or 400 if the update fails.
    """

    update_product = product_service.update_product(product_id, product_data)

    if not update_product:
        HTTPException(status_code=400, detail="Update error!")

    return update_product


@product_route.delete("/product/{id_product}")
async def delete_user(
    id_product: int, product_service: ProductService = Depends(get_product_service)
):
    """
    Delete a product by ID.

    This endpoint deletes the product identified by the given product ID.

    Parameters:
    - id_product (int): The ID of the product to be deleted.
    - product_service (ProductService): Dependency that provides the product service instance to perform deletion.

    Responses:
    - 200 OK: Returns a success message when the product is deleted.
    - 400 Bad Request: If the product deletion fails, a `400` status is returned with the message "product not deleted!".

    Example usage:
    - Request: DELETE /product/{id_product}
    - Response: Confirmation message or 400 if deletion fails.
    """
    delete_service = product_service.delete_product(id_product)

    if not delete_service:
        HTTPException(status_code=400, detail="product not deleted!")
    return JSONResponse(content={"message": "Deleted successefuly!"}, status_code=200)
