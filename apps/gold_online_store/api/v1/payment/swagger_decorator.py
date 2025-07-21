from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.gold_online_store.serializers import PaymentTransactionSerializer

# PaymentTransactionAdminAPIView Decorators
admin_create_payment_transaction_swagger = swagger_auto_schema(
    operation_summary='Create a New Payment Transaction (Admin)',
    operation_description=(
        'This endpoint allows administrators to create a new payment transaction for a user. '
        'The request must include the user ID, money_amount, and status (PENDING, SUCCESS, or FAILED). '
        'The money_amount must be non-negative and within reasonable limits. '
        'The payment_date is automatically set to the current time if not provided. '
        'The response returns the created transaction’s details, including the user and status display. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.payment_transaction'],
    request_body=PaymentTransactionSerializer,
    responses={
        201: PaymentTransactionSerializer,
        400: 'Invalid input data (e.g., negative amount, invalid user ID, or invalid status).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_retrieve_payment_transaction_swagger = swagger_auto_schema(
    operation_summary='Retrieve Payment Transaction Details (Admin)',
    operation_description=(
        'This endpoint allows administrators to retrieve detailed information about a specific payment transaction by its ID. '
        'The response includes details such as ID, associated user, payment_date, money_amount, status, and status display. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.payment_transaction'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the payment transaction to retrieve.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: PaymentTransactionSerializer,
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Payment transaction with the specified ID does not exist.'
    }
)

admin_update_payment_transaction_swagger = swagger_auto_schema(
    operation_summary='Fully Update a Payment Transaction (Admin)',
    operation_description=(
        'This endpoint allows administrators to fully update the details of an existing payment transaction identified by its ID. '
        'The request body must include all required fields (e.g., user, money_amount, status) even if some fields remain unchanged. '
        'The money_amount must be non-negative and within reasonable limits, and status must be one of PENDING, SUCCESS, or FAILED. '
        'The response returns the updated transaction’s details. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.payment_transaction'],
    request_body=PaymentTransactionSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the payment transaction to update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: PaymentTransactionSerializer,
        400: 'Invalid input data (e.g., negative amount or invalid status).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Payment transaction with the specified ID does not exist.'
    }
)

admin_partial_update_payment_transaction_swagger = swagger_auto_schema(
    operation_summary='Partially Update a Payment Transaction (Admin)',
    operation_description=(
        'This endpoint allows administrators to partially update the details of an existing payment transaction identified by its ID. '
        'Only the provided fields in the request body will be updated (e.g., updating only money_amount or status). '
        'The money_amount must be non-negative and within reasonable limits, and status must be one of PENDING, SUCCESS, or FAILED. '
        'The response returns the updated transaction’s details. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.payment_transaction'],
    request_body=PaymentTransactionSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the payment transaction to partially update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: PaymentTransactionSerializer,
        400: 'Invalid input data (e.g., negative amount or invalid status).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Payment transaction with the specified ID does not exist.'
    }
)

admin_destroy_payment_transaction_swagger = swagger_auto_schema(
    operation_summary='Delete a Payment Transaction (Admin)',
    operation_description=(
        'This endpoint allows administrators to delete a payment transaction by its ID. '
        'The operation permanently removes the transaction from the system. '
        'A successful deletion returns a 204 No Content response. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.payment_transaction'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the payment transaction to delete.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        204: 'Payment transaction successfully deleted.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Payment transaction with the specified ID does not exist.'
    }
)

admin_list_payment_transaction_swagger = swagger_auto_schema(
    operation_summary='List All Payment Transactions (Admin)',
    operation_description=(
        'This endpoint allows administrators to retrieve a list of all payment transaction records in the system. '
        'The response includes details for each transaction, such as ID, associated user, payment_date, money_amount, status, and status display. '
        'Optional search functionality is available using the "search" query parameter to filter transactions by username or status. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.payment_transaction'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter transactions by username or status (partial match).", type=openapi.TYPE_STRING)
    ],
    responses={
        200: PaymentTransactionSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

# PaymentTransactionAPIView Decorators
user_create_payment_transaction_swagger = swagger_auto_schema(
    operation_summary='Create a New Payment Transaction (User)',
    operation_description=(
        'This endpoint allows authenticated users to create a new payment transaction for themselves. '
        'The request must include money_amount and status (PENDING, SUCCESS, or FAILED). '
        'The money_amount must be non-negative and within reasonable limits. '
        'The payment_date is automatically set to the current time if not provided. '
        'The user field is automatically set to the authenticated user and cannot be modified. '
        'The response returns the created transaction’s details, including status display. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.payment_transaction'],
    request_body=PaymentTransactionSerializer,
    responses={
        201: PaymentTransactionSerializer,
        400: 'Invalid input data (e.g., negative amount or invalid status).',
        401: 'Unauthorized: Valid JWT token required.'
    }
)

user_retrieve_payment_transaction_swagger = swagger_auto_schema(
    operation_summary='Retrieve Own Payment Transaction Details',
    operation_description=(
        'This endpoint allows authenticated users to retrieve their own payment transaction information by its ID. '
        'The response includes details such as ID, associated user, payment_date, money_amount, status, and status display. '
        'The transaction ID must correspond to a transaction belonging to the authenticated user, and users cannot access other users’ transactions. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.payment_transaction'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s payment transaction.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: PaymentTransactionSerializer,
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only access their own payment transaction.',
        404: 'Not Found: Payment transaction with the specified ID does not exist.'
    }
)

user_update_payment_transaction_swagger = swagger_auto_schema(
    operation_summary='Fully Update Own Payment Transaction',
    operation_description=(
        'This endpoint allows authenticated users to fully update their own payment transaction identified by its ID. '
        'The request body must include all required fields (e.g., money_amount, status) even if some fields remain unchanged. '
        'The money_amount must be non-negative and within reasonable limits, and status must be one of PENDING, SUCCESS, or FAILED. '
        'The user field cannot be modified and must match the authenticated user. '
        'The response returns the updated transaction’s details. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.payment_transaction'],
    request_body=PaymentTransactionSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s payment transaction to update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: PaymentTransactionSerializer,
        400: 'Invalid input data (e.g., negative amount or invalid status).',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only update their own payment transaction.',
        404: 'Not Found: Payment transaction with the specified ID does not exist.'
    }
)

user_partial_update_payment_transaction_swagger = swagger_auto_schema(
    operation_summary='Partially Update Own Payment Transaction',
    operation_description=(
        'This endpoint allows authenticated users to partially update their own payment transaction identified by its ID. '
        'Only the provided fields in the request body will be updated (e.g., updating only money_amount or status). '
        'The money_amount must be non-negative and within reasonable limits, and status must be one of PENDING, SUCCESS, or FAILED. '
        'The user field cannot be modified and must match the authenticated user. '
        'The response returns the updated transaction’s details. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.payment_transaction'],
    request_body=PaymentTransactionSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s payment transaction to partially update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: PaymentTransactionSerializer,
        400: 'Invalid input data (e.g., negative amount or invalid status).',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only update their own payment transaction.',
        404: 'Not Found: Payment transaction with the specified ID does not exist.'
    }
)

user_destroy_payment_transaction_swagger = swagger_auto_schema(
    operation_summary='Delete Own Payment Transaction',
    operation_description=(
        'This endpoint allows authenticated users to delete their own payment transaction by its ID. '
        'The operation permanently removes the transaction from the system. '
        'The transaction ID must correspond to a transaction belonging to the authenticated user. '
        'A successful deletion returns a 204 No Content response. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.payment_transaction'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s payment transaction to delete.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        204: 'Payment transaction successfully deleted.',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only delete their own payment transaction.',
        404: 'Not Found: Payment transaction with the specified ID does not exist.'
    }
)

user_list_payment_transaction_swagger = swagger_auto_schema(
    operation_summary='List Own Payment Transactions',
    operation_description=(
        'This endpoint allows authenticated users to retrieve a list of their own payment transaction records. '
        'The response includes details for each transaction, such as ID, associated user, payment_date, money_amount, status, and status display. '
        'Optional search functionality is available using the "search" query parameter to filter transactions by status. '
        'Users can only access their own transactions. This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.payment_transaction'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter transactions by status (partial match).", type=openapi.TYPE_STRING)
    ],
    responses={
        200: PaymentTransactionSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only access their own payment transactions.'
    }
)