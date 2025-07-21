from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.gold_online_store.serializers import GoldSaleTransactionSerializer, GoldPurchaseTransactionSerializer

# GoldSaleTransactionAdminAPIView Decorators
admin_create_gold_sale_transaction_swagger = swagger_auto_schema(
    operation_summary='Create a New Gold Sale Transaction (Admin)',
    operation_description=(
        'This endpoint allows administrators to create a new gold sale transaction for a user. '
        'The request must include the user ID, money_amount, gold_amount, gold_price ID, and status (ACCEPTED, WAITING, or REJECTED). '
        'The money_amount and gold_amount must be non-negative and within reasonable limits. '
        'The create_date is automatically set to the current time if not provided. '
        'The response returns the created transaction’s details, including the user and status display. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.gold_sale_transaction'],
    request_body=GoldSaleTransactionSerializer,
    responses={
        201: GoldSaleTransactionSerializer,
        400: 'Invalid input data (e.g., negative amounts, invalid user ID, or invalid status).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_retrieve_gold_sale_transaction_swagger = swagger_auto_schema(
    operation_summary='Retrieve Gold Sale Transaction Details (Admin)',
    operation_description=(
        'This endpoint allows administrators to retrieve detailed information about a specific gold sale transaction by its ID. '
        'The response includes details such as ID, associated user, create_date, money_amount, gold_amount, gold_price, status, and status display. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.gold_sale_transaction'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the gold sale transaction to retrieve.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: GoldSaleTransactionSerializer,
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Gold sale transaction with the specified ID does not exist.'
    }
)

admin_update_gold_sale_transaction_swagger = swagger_auto_schema(
    operation_summary='Fully Update a Gold Sale Transaction (Admin)',
    operation_description=(
        'This endpoint allows administrators to fully update the details of an existing gold sale transaction identified by its ID. '
        'The request body must include all required fields (e.g., user, money_amount, gold_amount, gold_price, status) even if some fields remain unchanged. '
        'The money_amount and gold_amount must be non-negative, and status must be one of ACCEPTED, WAITING, or REJECTED. '
        'The response returns the updated transaction’s details. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.gold_sale_transaction'],
    request_body=GoldSaleTransactionSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the gold sale transaction to update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: GoldSaleTransactionSerializer,
        400: 'Invalid input data (e.g., negative amounts or invalid status).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Gold sale transaction with the specified ID does not exist.'
    }
)

admin_partial_update_gold_sale_transaction_swagger = swagger_auto_schema(
    operation_summary='Partially Update a Gold Sale Transaction (Admin)',
    operation_description=(
        'This endpoint allows administrators to partially update the details of an existing gold sale transaction identified by its ID. '
        'Only the provided fields in the request body will be updated (e.g., updating only money_amount or status). '
        'The money_amount and gold_amount must be non-negative, and status must be one of ACCEPTED, WAITING, or REJECTED. '
        'The response returns the updated transaction’s details. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.gold_sale_transaction'],
    request_body=GoldSaleTransactionSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the gold sale transaction to partially update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: GoldSaleTransactionSerializer,
        400: 'Invalid input data (e.g., negative amounts or invalid status).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Gold sale transaction with the specified ID does not exist.'
    }
)

admin_destroy_gold_sale_transaction_swagger = swagger_auto_schema(
    operation_summary='Delete a Gold Sale Transaction (Admin)',
    operation_description=(
        'This endpoint allows administrators to delete a gold sale transaction by its ID. '
        'The operation permanently removes the transaction from the system. '
        'A successful deletion returns a 204 No Content response. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.gold_sale_transaction'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the gold sale transaction to delete.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        204: 'Gold sale transaction successfully deleted.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Gold sale transaction with the specified ID does not exist.'
    }
)

admin_list_gold_sale_transaction_swagger = swagger_auto_schema(
    operation_summary='List All Gold Sale Transactions (Admin)',
    operation_description=(
        'This endpoint allows administrators to retrieve a list of all gold sale transaction records in the system. '
        'The response includes details for each transaction, such as ID, associated user, create_date, money_amount, gold_amount, gold_price, status, and status display. '
        'Optional search functionality is available using the "search" query parameter to filter transactions by username or status. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.gold_sale_transaction'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter transactions by username or status (partial match).", type=openapi.TYPE_STRING)
    ],
    responses={
        200: GoldSaleTransactionSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

# GoldSaleTransactionAPIView Decorators
user_create_gold_sale_transaction_swagger = swagger_auto_schema(
    operation_summary='Create a New Gold Sale Transaction (User)',
    operation_description=(
        'This endpoint allows authenticated users to create a new gold sale transaction for themselves. '
        'The request must include money_amount, gold_amount, gold_price ID, and status (ACCEPTED, WAITING, or REJECTED). '
        'The money_amount and gold_amount must be non-negative and within reasonable limits. '
        'The create_date is automatically set to the current time if not provided. '
        'The user field is automatically set to the authenticated user and cannot be modified. '
        'The response returns the created transaction’s details, including status display. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.gold_sale_transaction'],
    request_body=GoldSaleTransactionSerializer,
    responses={
        201: GoldSaleTransactionSerializer,
        400: 'Invalid input data (e.g., negative amounts or invalid status).',
        401: 'Unauthorized: Valid JWT token required.'
    }
)

user_retrieve_gold_sale_transaction_swagger = swagger_auto_schema(
    operation_summary='Retrieve Own Gold Sale Transaction Details',
    operation_description=(
        'This endpoint allows authenticated users to retrieve their own gold sale transaction information by its ID. '
        'The response includes details such as ID, associated user, create_date, money_amount, gold_amount, gold_price, status, and status display. '
        'The transaction ID must correspond to a transaction belonging to the authenticated user, and users cannot access other users’ transactions. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.gold_sale_transaction'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s gold sale transaction.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: GoldSaleTransactionSerializer,
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only access their own gold sale transaction.',
        404: 'Not Found: Gold sale transaction with the specified ID does not exist.'
    }
)

user_update_gold_sale_transaction_swagger = swagger_auto_schema(
    operation_summary='Fully Update Own Gold Sale Transaction',
    operation_description=(
        'This endpoint allows authenticated users to fully update their own gold sale transaction identified by its ID. '
        'The request body must include all required fields (e.g., money_amount, gold_amount, gold_price, status) even if some fields remain unchanged. '
        'The money_amount and gold_amount must be non-negative, and status must be one of ACCEPTED, WAITING, or REJECTED. '
        'The user field cannot be modified and must match the authenticated user. '
        'The response returns the updated transaction’s details. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.gold_sale_transaction'],
    request_body=GoldSaleTransactionSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s gold sale transaction to update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: GoldSaleTransactionSerializer,
        400: 'Invalid input data (e.g., negative amounts or invalid status).',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only update their own gold sale transaction.',
        404: 'Not Found: Gold sale transaction with the specified ID does not exist.'
    }
)

user_partial_update_gold_sale_transaction_swagger = swagger_auto_schema(
    operation_summary='Partially Update Own Gold Sale Transaction',
    operation_description=(
        'This endpoint allows authenticated users to partially update their own gold sale transaction identified by its ID. '
        'Only the provided fields in the request body will be updated (e.g., updating only money_amount or status). '
        'The money_amount and gold_amount must be non-negative, and status must be one of ACCEPTED, WAITING, or REJECTED. '
        'The user field cannot be modified and must match the authenticated user. '
        'The response returns the updated transaction’s details. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.gold_sale_transaction'],
    request_body=GoldSaleTransactionSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s gold sale transaction to partially update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: GoldSaleTransactionSerializer,
        400: 'Invalid input data (e.g., negative amounts or invalid status).',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only update their own gold sale transaction.',
        404: 'Not Found: Gold sale transaction with the specified ID does not exist.'
    }
)

user_destroy_gold_sale_transaction_swagger = swagger_auto_schema(
    operation_summary='Delete Own Gold Sale Transaction',
    operation_description=(
        'This endpoint allows authenticated users to delete their own gold sale transaction by its ID. '
        'The operation permanently removes the transaction from the system. '
        'The transaction ID must correspond to a transaction belonging to the authenticated user. '
        'A successful deletion returns a 204 No Content response. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.gold_sale_transaction'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s gold sale transaction to delete.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        204: 'Gold sale transaction successfully deleted.',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only delete their own gold sale transaction.',
        404: 'Not Found: Gold sale transaction with the specified ID does not exist.'
    }
)

user_list_gold_sale_transaction_swagger = swagger_auto_schema(
    operation_summary='List Own Gold Sale Transactions',
    operation_description=(
        'This endpoint allows authenticated users to retrieve a list of their own gold sale transaction records. '
        'The response includes details for each transaction, such as ID, associated user, create_date, money_amount, gold_amount, gold_price, status, and status display. '
        'Optional search functionality is available using the "search" query parameter to filter transactions by status. '
        'Users can only access their own transactions. This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.gold_sale_transaction'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter transactions by status (partial match).", type=openapi.TYPE_STRING)
    ],
    responses={
        200: GoldSaleTransactionSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only access their own gold sale transactions.'
    }
)

# GoldPurchaseTransactionAdminAPIView Decorators
admin_create_gold_purchase_transaction_swagger = swagger_auto_schema(
    operation_summary='Create a New Gold Purchase Transaction (Admin)',
    operation_description=(
        'This endpoint allows administrators to create a new gold purchase transaction for a user. '
        'The request must include the user ID, money_amount, gold_amount, gold_price ID, and status (ACCEPTED, WAITING, or REJECTED). '
        'The money_amount and gold_amount must be non-negative and within reasonable limits. '
        'The create_date is automatically set to the current time if not provided. '
        'The response returns the created transaction’s details, including the user and status display. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.gold_purchase_transaction'],
    request_body=GoldPurchaseTransactionSerializer,
    responses={
        201: GoldPurchaseTransactionSerializer,
        400: 'Invalid input data (e.g., negative amounts, invalid user ID, or invalid status).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_retrieve_gold_purchase_transaction_swagger = swagger_auto_schema(
    operation_summary='Retrieve Gold Purchase Transaction Details (Admin)',
    operation_description=(
        'This endpoint allows administrators to retrieve detailed information about a specific gold purchase transaction by its ID. '
        'The response includes details such as ID, associated user, create_date, money_amount, gold_amount, gold_price, status, and status display. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.gold_purchase_transaction'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the gold purchase transaction to retrieve.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: GoldPurchaseTransactionSerializer,
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Gold purchase transaction with the specified ID does not exist.'
    }
)

admin_update_gold_purchase_transaction_swagger = swagger_auto_schema(
    operation_summary='Fully Update a Gold Purchase Transaction (Admin)',
    operation_description=(
        'This endpoint allows administrators to fully update the details of an existing gold purchase transaction identified by its ID. '
        'The request body must include all required fields (e.g., user, money_amount, gold_amount, gold_price, status) even if some fields remain unchanged. '
        'The money_amount and gold_amount must be non-negative, and status must be one of ACCEPTED, WAITING, or REJECTED. '
        'The response returns the updated transaction’s details. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.gold_purchase_transaction'],
    request_body=GoldPurchaseTransactionSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the gold purchase transaction to update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: GoldPurchaseTransactionSerializer,
        400: 'Invalid input data (e.g., negative amounts or invalid status).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Gold purchase transaction with the specified ID does not exist.'
    }
)

admin_partial_update_gold_purchase_transaction_swagger = swagger_auto_schema(
    operation_summary='Partially Update a Gold Purchase Transaction (Admin)',
    operation_description=(
        'This endpoint allows administrators to partially update the details of an existing gold purchase transaction identified by its ID. '
        'Only the provided fields in the request body will be updated (e.g., updating only money_amount or status). '
        'The money_amount and gold_amount must be non-negative, and status must be one of ACCEPTED, WAITING, or REJECTED. '
        'The response returns the updated transaction’s details. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.gold_purchase_transaction'],
    request_body=GoldPurchaseTransactionSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the gold purchase transaction to partially update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: GoldPurchaseTransactionSerializer,
        400: 'Invalid input data (e.g., negative amounts or invalid status).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Gold purchase transaction with the specified ID does not exist.'
    }
)

admin_destroy_gold_purchase_transaction_swagger = swagger_auto_schema(
    operation_summary='Delete a Gold Purchase Transaction (Admin)',
    operation_description=(
        'This endpoint allows administrators to delete a gold purchase transaction by its ID. '
        'The operation permanently removes the transaction from the system. '
        'A successful deletion returns a 204 No Content response. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.gold_purchase_transaction'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the gold purchase transaction to delete.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        204: 'Gold purchase transaction successfully deleted.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Gold purchase transaction with the specified ID does not exist.'
    }
)

admin_list_gold_purchase_transaction_swagger = swagger_auto_schema(
    operation_summary='List All Gold Purchase Transactions (Admin)',
    operation_description=(
        'This endpoint allows administrators to retrieve a list of all gold purchase transaction records in the system. '
        'The response includes details for each transaction, such as ID, associated user, create_date, money_amount, gold_amount, gold_price, status, and status display. '
        'Optional search functionality is available using the "search" query parameter to filter transactions by username or status. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.gold_purchase_transaction'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter transactions by username or status (partial match).", type=openapi.TYPE_STRING)
    ],
    responses={
        200: GoldPurchaseTransactionSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

# GoldPurchaseTransactionAPIView Decorators
user_create_gold_purchase_transaction_swagger = swagger_auto_schema(
    operation_summary='Create a New Gold Purchase Transaction (User)',
    operation_description=(
        'This endpoint allows authenticated users to create a new gold purchase transaction for themselves. '
        'The request must include money_amount, gold_amount, gold_price ID, and status (ACCEPTED, WAITING, or REJECTED). '
        'The money_amount and gold_amount must be non-negative and within reasonable limits. '
        'The create_date is automatically set to the current time if not provided. '
        'The user field is automatically set to the authenticated user and cannot be modified. '
        'The response returns the created transaction’s details, including status display. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.gold_purchase_transaction'],
    request_body=GoldPurchaseTransactionSerializer,
    responses={
        201: GoldPurchaseTransactionSerializer,
        400: 'Invalid input data (e.g., negative amounts or invalid status).',
        401: 'Unauthorized: Valid JWT token required.'
    }
)

user_retrieve_gold_purchase_transaction_swagger = swagger_auto_schema(
    operation_summary='Retrieve Own Gold Purchase Transaction Details',
    operation_description=(
        'This endpoint allows authenticated users to retrieve their own gold purchase transaction information by its ID. '
        'The response includes details such as ID, associated user, create_date, money_amount, gold_amount, gold_price, status, and status display. '
        'The transaction ID must correspond to a transaction belonging to the authenticated user, and users cannot access other users’ transactions. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.gold_purchase_transaction'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s gold purchase transaction.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: GoldPurchaseTransactionSerializer,
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only access their own gold purchase transaction.',
        404: 'Not Found: Gold purchase transaction with the specified ID does not exist.'
    }
)

user_update_gold_purchase_transaction_swagger = swagger_auto_schema(
    operation_summary='Fully Update Own Gold Purchase Transaction',
    operation_description=(
        'This endpoint allows authenticated users to fully update their own gold purchase transaction identified by its ID. '
        'The request body must include all required fields (e.g., money_amount, gold_amount, gold_price, status) even if some fields remain unchanged. '
        'The money_amount and gold_amount must be non-negative, and status must be one of ACCEPTED, WAITING, or REJECTED. '
        'The user field cannot be modified and must match the authenticated user. '
        'The response returns the updated transaction’s details. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.gold_purchase_transaction'],
    request_body=GoldPurchaseTransactionSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s gold purchase transaction to update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: GoldPurchaseTransactionSerializer,
        400: 'Invalid input data (e.g., negative amounts or invalid status).',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only update their own gold purchase transaction.',
        404: 'Not Found: Gold purchase transaction with the specified ID does not exist.'
    }
)

user_partial_update_gold_purchase_transaction_swagger = swagger_auto_schema(
    operation_summary='Partially Update Own Gold Purchase Transaction',
    operation_description=(
        'This endpoint allows authenticated users to partially update their own gold purchase transaction identified by its ID. '
        'Only the provided fields in the request body will be updated (e.g., updating only money_amount or status). '
        'The money_amount and gold_amount must be non-negative, and status must be one of ACCEPTED, WAITING, or REJECTED. '
        'The user field cannot be modified and must match the authenticated user. '
        'The response returns the updated transaction’s details. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.gold_purchase_transaction'],
    request_body=GoldPurchaseTransactionSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s gold purchase transaction to partially update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: GoldPurchaseTransactionSerializer,
        400: 'Invalid input data (e.g., negative amounts or invalid status).',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only update their own gold purchase transaction.',
        404: 'Not Found: Gold purchase transaction with the specified ID does not exist.'
    }
)

user_destroy_gold_purchase_transaction_swagger = swagger_auto_schema(
    operation_summary='Delete Own Gold Purchase Transaction',
    operation_description=(
        'This endpoint allows authenticated users to delete their own gold purchase transaction by its ID. '
        'The operation permanently removes the transaction from the system. '
        'The transaction ID must correspond to a transaction belonging to the authenticated user. '
        'A successful deletion returns a 204 No Content response. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.gold_purchase_transaction'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s gold purchase transaction to delete.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        204: 'Gold purchase transaction successfully deleted.',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only delete their own gold purchase transaction.',
        404: 'Not Found: Gold purchase transaction with the specified ID does not exist.'
    }
)

user_list_gold_purchase_transaction_swagger = swagger_auto_schema(
    operation_summary='List Own Gold Purchase Transactions',
    operation_description=(
        'This endpoint allows authenticated users to retrieve a list of their own gold purchase transaction records. '
        'The response includes details for each transaction, such as ID, associated user, create_date, money_amount, gold_amount, gold_price, status, and status display. '
        'Optional search functionality is available using the "search" query parameter to filter transactions by status. '
        'Users can only access their own transactions. This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.gold_purchase_transaction'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter transactions by status (partial match).", type=openapi.TYPE_STRING)
    ],
    responses={
        200: GoldPurchaseTransactionSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only access their own gold purchase transactions.'
    }
)