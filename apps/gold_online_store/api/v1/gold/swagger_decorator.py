from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.gold_online_store.serializers.gold import WalletSerializer, GoldPriceSerializer

# WalletAdminAPIView Decorators
admin_create_wallet_swagger = swagger_auto_schema(
    operation_summary='Create a New Wallet (Admin)',
    operation_description=(
        'This endpoint allows administrators to create a new wallet for a user. '
        'The request must include the user ID, money_stock, and gold_stock. '
        'The money_stock and gold_stock must be non-negative and within reasonable limits. '
        'The response returns the created wallet’s details, including the total value calculated based on the latest active gold price. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.wallet'],
    request_body=WalletSerializer,
    responses={
        201: WalletSerializer,
        400: 'Invalid input data (e.g., negative amounts or invalid user ID).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_retrieve_wallet_swagger = swagger_auto_schema(
    operation_summary='Retrieve Wallet Details (Admin)',
    operation_description=(
        'This endpoint allows administrators to retrieve detailed information about a specific wallet by its ID. '
        'The response includes wallet details such as ID, associated user, money_stock, gold_stock, and total_value. '
        'The total_value is calculated using the latest active gold price. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.wallet'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the wallet to retrieve.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: WalletSerializer,
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Wallet with the specified ID does not exist.'
    }
)

admin_update_wallet_swagger = swagger_auto_schema(
    operation_summary='Fully Update a Wallet (Admin)',
    operation_description=(
        'This endpoint allows administrators to fully update the details of an existing wallet identified by its ID. '
        'The request body must include all required fields (e.g., user, money_stock, gold_stock) even if some fields remain unchanged. '
        'The money_stock and gold_stock must be non-negative and within reasonable limits. '
        'The response returns the updated wallet’s details, including the total value. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.wallet'],
    request_body=WalletSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the wallet to update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: WalletSerializer,
        400: 'Invalid input data (e.g., negative amounts or invalid user ID).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Wallet with the specified ID does not exist.'
    }
)

admin_partial_update_wallet_swagger = swagger_auto_schema(
    operation_summary='Partially Update a Wallet (Admin)',
    operation_description=(
        'This endpoint allows administrators to partially update the details of an existing wallet identified by its ID. '
        'Only the provided fields in the request body will be updated (e.g., updating only money_stock or gold_stock). '
        'The money_stock and gold_stock must be non-negative and within reasonable limits. '
        'The response returns the updated wallet’s details, including the total value. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.wallet'],
    request_body=WalletSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the wallet to partially update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: WalletSerializer,
        400: 'Invalid input data (e.g., negative amounts).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Wallet with the specified ID does not exist.'
    }
)

admin_destroy_wallet_swagger = swagger_auto_schema(
    operation_summary='Delete a Wallet (Admin)',
    operation_description=(
        'This endpoint allows administrators to delete a wallet by its ID. '
        'The operation permanently removes the wallet from the system. '
        'A successful deletion returns a 204 No Content response. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.wallet'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the wallet to delete.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        204: 'Wallet successfully deleted.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Wallet with the specified ID does not exist.'
    }
)

admin_list_wallet_swagger = swagger_auto_schema(
    operation_summary='List All Wallets (Admin)',
    operation_description=(
        'This endpoint allows administrators to retrieve a list of all wallet records in the system. '
        'The response includes details for each wallet, such as ID, associated user, money_stock, gold_stock, and total_value. '
        'Optional search functionality is available using the "search" query parameter to filter wallets by username. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.wallet'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter wallets by username (partial match).", type=openapi.TYPE_STRING)
    ],
    responses={
        200: WalletSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

# WalletAPIView Decorators
user_create_wallet_swagger = swagger_auto_schema(
    operation_summary='Create a New Wallet (User)',
    operation_description=(
        'This endpoint allows authenticated users to create a new wallet for themselves. '
        'The request must include money_stock and gold_stock, both of which must be non-negative and within reasonable limits. '
        'The user field is automatically set to the authenticated user and cannot be modified. '
        'The response returns the created wallet’s details, including the total value calculated based on the latest active gold price. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.wallet'],
    request_body=WalletSerializer,
    responses={
        201: WalletSerializer,
        400: 'Invalid input data (e.g., negative amounts or attempting to set user field).',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only create their own wallet.'
    }
)

user_retrieve_wallet_swagger = swagger_auto_schema(
    operation_summary='Retrieve Own Wallet Details',
    operation_description=(
        'This endpoint allows authenticated users to retrieve their own wallet information by its ID. '
        'The response includes details such as ID, associated user, money_stock, gold_stock, and total_value (calculated using the latest active gold price). '
        'The wallet ID must correspond to the authenticated user’s wallet, and users cannot access other users’ wallets. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.wallet'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s wallet.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: WalletSerializer,
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only access their own wallet.',
        404: 'Not Found: Wallet with the specified ID does not exist.'
    }
)

user_update_wallet_swagger = swagger_auto_schema(
    operation_summary='Fully Update Own Wallet',
    operation_description=(
        'This endpoint allows authenticated users to fully update their own wallet identified by its ID. '
        'The request body must include all required fields (e.g., money_stock, gold_stock) even if some fields remain unchanged. '
        'The money_stock and gold_stock must be non-negative and within reasonable limits. '
        'The user field cannot be modified and must match the authenticated user. '
        'The response returns the updated wallet’s details, including the total value. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.wallet'],
    request_body=WalletSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s wallet to update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: WalletSerializer,
        400: 'Invalid input data (e.g., negative amounts or attempting to modify user field).',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only update their own wallet.',
        404: 'Not Found: Wallet with the specified ID does not exist.'
    }
)

user_partial_update_wallet_swagger = swagger_auto_schema(
    operation_summary='Partially Update Own Wallet',
    operation_description=(
        'This endpoint allows authenticated users to partially update their own wallet identified by its ID. '
        'Only the provided fields in the request body will be updated (e.g., updating only money_stock or gold_stock). '
        'The money_stock and gold_stock must be non-negative and within reasonable limits. '
        'The user field cannot be modified and must match the authenticated user. '
        'The response returns the updated wallet’s details, including the total value. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.wallet'],
    request_body=WalletSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s wallet to partially update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: WalletSerializer,
        400: 'Invalid input data (e.g., negative amounts or attempting to modify user field).',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only update their own wallet.',
        404: 'Not Found: Wallet with the specified ID does not exist.'
    }
)

user_destroy_wallet_swagger = swagger_auto_schema(
    operation_summary='Delete Own Wallet',
    operation_description=(
        'This endpoint allows authenticated users to delete their own wallet by its ID. '
        'The operation permanently removes the wallet from the system. '
        'The wallet ID must correspond to the authenticated user’s wallet. '
        'A successful deletion returns a 204 No Content response. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.wallet'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s wallet to delete.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        204: 'Wallet successfully deleted.',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only delete their own wallet.',
        404: 'Not Found: Wallet with the specified ID does not exist.'
    }
)

user_list_wallet_swagger = swagger_auto_schema(
    operation_summary='List Own Wallet',
    operation_description=(
        'This endpoint allows authenticated users to retrieve their own wallet record. '
        'The response includes details such as ID, associated user, money_stock, gold_stock, and total_value (calculated using the latest active gold price). '
        'Users can only access their own wallet. This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.wallet'],
    responses={
        200: WalletSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only access their own wallet.'
    }
)

# GoldPriceAdminAPIView Decorators
admin_create_gold_price_swagger = swagger_auto_schema(
    operation_summary='Create a New Gold Price (Admin)',
    operation_description=(
        'This endpoint allows administrators to create a new gold price record. '
        'The request must include sale_price, price_difference, total_gold_stock, stock_status, and active status. '
        'All monetary and stock values must be non-negative. If active is set to true, any existing active gold price will be deactivated. '
        'The response returns the created gold price details. '
        'This operation is restricted to admin users only and requires JWT authentication. Non-admin users have no access.'
    ),
    tags=['admin.gold_online_store.gold_price'],
    request_body=GoldPriceSerializer,
    responses={
        201: GoldPriceSerializer,
        400: 'Invalid input data (e.g., negative values or invalid fields).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_retrieve_gold_price_swagger = swagger_auto_schema(
    operation_summary='Retrieve Gold Price Details (Admin)',
    operation_description=(
        'This endpoint allows administrators to retrieve detailed information about a specific gold price record by its ID. '
        'The response includes details such as ID, date, sale_price, price_difference, total_gold_stock, stock_status, and active status. '
        'This operation is restricted to admin users only and requires JWT authentication. Non-admin users have no access.'
    ),
    tags=['admin.gold_online_store.gold_price'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the gold price record to retrieve.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: GoldPriceSerializer,
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Gold price record with the specified ID does not exist.'
    }
)

admin_update_gold_price_swagger = swagger_auto_schema(
    operation_summary='Fully Update a Gold Price (Admin)',
    operation_description=(
        'This endpoint allows administrators to fully update the details of an existing gold price record identified by its ID. '
        'The request body must include all required fields (e.g., sale_price, price_difference, total_gold_stock) even if some fields remain unchanged. '
        'All monetary and stock values must be non-negative. If active is set to true, any existing active gold price will be deactivated. '
        'The response returns the updated gold price details. '
        'This operation is restricted to admin users only and requires JWT authentication. Non-admin users have no access.'
    ),
    tags=['admin.gold_online_store.gold_price'],
    request_body=GoldPriceSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the gold price record to update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: GoldPriceSerializer,
        400: 'Invalid input data (e.g., negative values or invalid fields).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Gold price record with the specified ID does not exist.'
    }
)

admin_partial_update_gold_price_swagger = swagger_auto_schema(
    operation_summary='Partially Update a Gold Price (Admin)',
    operation_description=(
        'This endpoint allows administrators to partially update the details of an existing gold price record identified by its ID. '
        'Only the provided fields in the request body will be updated (e.g., updating only sale_price or stock_status). '
        'All monetary and stock values must be non-negative. If active is set to true, any existing active gold price will be deactivated. '
        'The response returns the updated gold price details. '
        'This operation is restricted to admin users only and requires JWT authentication. Non-admin users have no access.'
    ),
    tags=['admin.gold_online_store.gold_price'],
    request_body=GoldPriceSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the gold price record to partially update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: GoldPriceSerializer,
        400: 'Invalid input data (e.g., negative values).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Gold price record with the specified ID does not exist.'
    }
)

admin_destroy_gold_price_swagger = swagger_auto_schema(
    operation_summary='Delete a Gold Price (Admin)',
    operation_description=(
        'This endpoint allows administrators to delete a gold price record by its ID. '
        'The operation permanently removes the gold price from the system. '
        'A successful deletion returns a 204 No Content response. '
        'This operation is restricted to admin users only and requires JWT authentication. Non-admin users have no access.'
    ),
    tags=['admin.gold_online_store.gold_price'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the gold price record to delete.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        204: 'Gold price record successfully deleted.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Gold price record with the specified ID does not exist.'
    }
)

admin_list_gold_price_swagger = swagger_auto_schema(
    operation_summary='List All Gold Prices (Admin)',
    operation_description=(
        'This endpoint allows administrators to retrieve a list of all gold price records in the system. '
        'The response includes details for each record, such as ID, date, sale_price, price_difference, total_gold_stock, stock_status, and active status. '
        'Optional search functionality is available using the "search" query parameter to filter by date. '
        'This operation is restricted to admin users only and requires JWT authentication. Non-admin users have no access.'
    ),
    tags=['admin.gold_online_store.gold_price'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter gold prices by date (partial match in YYYY-MM-DD format).", type=openapi.TYPE_STRING)
    ],
    responses={
        200: GoldPriceSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)