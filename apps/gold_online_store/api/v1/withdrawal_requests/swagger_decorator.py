from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.gold_online_store.serializers.withdrawal_requests import MoneyWithdrawalRequestSerializer, GoldWithdrawalRequestSerializer

# MoneyWithdrawalRequestAdminAPIView Decorators
admin_create_money_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='Create a New Money Withdrawal Request (Admin)',
    operation_description=(
        'This endpoint allows administrators to create a new money withdrawal request for a user. '
        'The request must include the user ID, money_amount, and status (ACCEPTED, WAITING, or REJECTED). '
        'The money_amount must be non-negative and within reasonable limits. '
        'The create_date is automatically set to the current time if not provided. '
        'The response returns the created request’s details, including the user and status display. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.money_withdrawal_request'],
    request_body=MoneyWithdrawalRequestSerializer,
    responses={
        201: MoneyWithdrawalRequestSerializer,
        400: 'Invalid input data (e.g., negative amount, invalid user ID, or invalid status).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_retrieve_money_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='Retrieve Money Withdrawal Request Details (Admin)',
    operation_description=(
        'This endpoint allows administrators to retrieve detailed information about a specific money withdrawal request by its ID. '
        'The response includes details such as ID, associated user, create_date, money_amount, status, and status display. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.money_withdrawal_request'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the money withdrawal request to retrieve.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: MoneyWithdrawalRequestSerializer,
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Money withdrawal request with the specified ID does not exist.'
    }
)

admin_update_money_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='Fully Update a Money Withdrawal Request (Admin)',
    operation_description=(
        'This endpoint allows administrators to fully update the details of an existing money withdrawal request identified by its ID. '
        'The request body must include all required fields (e.g., user, money_amount, status) even if some fields remain unchanged. '
        'The money_amount must be non-negative, and status must be one of ACCEPTED, WAITING, or REJECTED. '
        'The response returns the updated request’s details. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.money_withdrawal_request'],
    request_body=MoneyWithdrawalRequestSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the money withdrawal request to update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: MoneyWithdrawalRequestSerializer,
        400: 'Invalid input data (e.g., negative amount or invalid status).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Money withdrawal request with the specified ID does not exist.'
    }
)

admin_partial_update_money_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='Partially Update a Money Withdrawal Request (Admin)',
    operation_description=(
        'This endpoint allows administrators to partially update the details of an existing money withdrawal request identified by its ID. '
        'Only the provided fields in the request body will be updated (e.g., updating only money_amount or status). '
        'The money_amount must be non-negative, and status must be one of ACCEPTED, WAITING, or REJECTED. '
        'The response returns the updated request’s details. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.money_withdrawal_request'],
    request_body=MoneyWithdrawalRequestSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the money withdrawal request to partially update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: MoneyWithdrawalRequestSerializer,
        400: 'Invalid input data (e.g., negative amount or invalid status).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Money withdrawal request with the specified ID does not exist.'
    }
)

admin_destroy_money_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='Delete a Money Withdrawal Request (Admin)',
    operation_description=(
        'This endpoint allows administrators to delete a money withdrawal request by its ID. '
        'The operation permanently removes the request from the system. '
        'A successful deletion returns a 204 No Content response. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.money_withdrawal_request'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the money withdrawal request to delete.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        204: 'Money withdrawal request successfully deleted.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Money withdrawal request with the specified ID does not exist.'
    }
)

admin_list_money_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='List All Money Withdrawal Requests (Admin)',
    operation_description=(
        'This endpoint allows administrators to retrieve a list of all money withdrawal request records in the system. '
        'The response includes details for each request, such as ID, associated user, create_date, money_amount, status, and status display. '
        'Optional search functionality is available using the "search" query parameter to filter requests by username or status. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.money_withdrawal_request'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter requests by username or status (partial match).", type=openapi.TYPE_STRING)
    ],
    responses={
        200: MoneyWithdrawalRequestSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

# MoneyWithdrawalRequestAPIView Decorators
user_create_money_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='Create a New Money Withdrawal Request (User)',
    operation_description=(
        'This endpoint allows authenticated users to create a new money withdrawal request for themselves. '
        'The request must include money_amount and status (ACCEPTED, WAITING, or REJECTED). '
        'The money_amount must be non-negative and within reasonable limits. '
        'The create_date is automatically set to the current time if not provided. '
        'The user field is automatically set to the authenticated user and cannot be modified. '
        'The response returns the created request’s details, including status display. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.money_withdrawal_request'],
    request_body=MoneyWithdrawalRequestSerializer,
    responses={
        201: MoneyWithdrawalRequestSerializer,
        400: 'Invalid input data (e.g., negative amount or invalid status).',
        401: 'Unauthorized: Valid JWT token required.'
    }
)

user_retrieve_money_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='Retrieve Own Money Withdrawal Request Details',
    operation_description=(
        'This endpoint allows authenticated users to retrieve their own money withdrawal request information by its ID. '
        'The response includes details such as ID, associated user, create_date, money_amount, status, and status display. '
        'The request ID must correspond to a request belonging to the authenticated user, and users cannot access other users’ requests. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.money_withdrawal_request'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s money withdrawal request.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: MoneyWithdrawalRequestSerializer,
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only access their own money withdrawal request.',
        404: 'Not Found: Money withdrawal request with the specified ID does not exist.'
    }
)

user_update_money_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='Fully Update Own Money Withdrawal Request',
    operation_description=(
        'This endpoint allows authenticated users to fully update their own money withdrawal request identified by its ID. '
        'The request body must include all required fields (e.g., money_amount, status) even if some fields remain unchanged. '
        'The money_amount must be non-negative, and status must be one of ACCEPTED, WAITING, or REJECTED. '
        'The user field cannot be modified and must match the authenticated user. '
        'The response returns the updated request’s details. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.money_withdrawal_request'],
    request_body=MoneyWithdrawalRequestSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s money withdrawal request to update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: MoneyWithdrawalRequestSerializer,
        400: 'Invalid input data (e.g., negative amount or invalid status).',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only update their own money withdrawal request.',
        404: 'Not Found: Money withdrawal request with the specified ID does not exist.'
    }
)

user_partial_update_money_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='Partially Update Own Money Withdrawal Request',
    operation_description=(
        'This endpoint allows authenticated users to partially update their own money withdrawal request identified by its ID. '
        'Only the provided fields in the request body will be updated (e.g., updating only money_amount or status). '
        'The money_amount must be non-negative, and status must be one of ACCEPTED, WAITING, or REJECTED. '
        'The user field cannot be modified and must match the authenticated user. '
        'The response returns the updated request’s details. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.money_withdrawal_request'],
    request_body=MoneyWithdrawalRequestSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s money withdrawal request to partially update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: MoneyWithdrawalRequestSerializer,
        400: 'Invalid input data (e.g., negative amount or invalid status).',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only update their own money withdrawal request.',
        404: 'Not Found: Money withdrawal request with the specified ID does not exist.'
    }
)

user_destroy_money_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='Delete Own Money Withdrawal Request',
    operation_description=(
        'This endpoint allows authenticated users to delete their own money withdrawal request by its ID. '
        'The operation permanently removes the request from the system. '
        'The request ID must correspond to a request belonging to the authenticated user. '
        'A successful deletion returns a 204 No Content response. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.money_withdrawal_request'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s money withdrawal request to delete.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        204: 'Money withdrawal request successfully deleted.',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only delete their own money withdrawal request.',
        404: 'Not Found: Money withdrawal request with the specified ID does not exist.'
    }
)

user_list_money_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='List Own Money Withdrawal Requests',
    operation_description=(
        'This endpoint allows authenticated users to retrieve a list of their own money withdrawal request records. '
        'The response includes details for each request, such as ID, associated user, create_date, money_amount, status, and status display. '
        'Optional search functionality is available using the "search" query parameter to filter requests by status. '
        'Users can only access their own requests. This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.money_withdrawal_request'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter requests by status (partial match).", type=openapi.TYPE_STRING)
    ],
    responses={
        200: MoneyWithdrawalRequestSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only access their own money withdrawal requests.'
    }
)

# GoldWithdrawalRequestAdminAPIView Decorators
admin_create_gold_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='Create a New Gold Withdrawal Request (Admin)',
    operation_description=(
        'This endpoint allows administrators to create a new gold withdrawal request for a user. '
        'The request must include the user ID, gold_amount, and status (ACCEPTED, WAITING, or REJECTED). '
        'The gold_amount must be non-negative and within reasonable limits. '
        'The create_date is automatically set to the current time if not provided. '
        'The response returns the created request’s details, including the user and status display. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.gold_withdrawal_request'],
    request_body=GoldWithdrawalRequestSerializer,
    responses={
        201: GoldWithdrawalRequestSerializer,
        400: 'Invalid input data (e.g., negative amount, invalid user ID, or invalid status).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_retrieve_gold_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='Retrieve Gold Withdrawal Request Details (Admin)',
    operation_description=(
        'This endpoint allows administrators to retrieve detailed information about a specific gold withdrawal request by its ID. '
        'The response includes details such as ID, associated user, create_date, gold_amount, status, and status display. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.gold_withdrawal_request'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the gold withdrawal request to retrieve.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: GoldWithdrawalRequestSerializer,
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Gold withdrawal request with the specified ID does not exist.'
    }
)

admin_update_gold_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='Fully Update a Gold Withdrawal Request (Admin)',
    operation_description=(
        'This endpoint allows administrators to fully update the details of an existing gold withdrawal request identified by its ID. '
        'The request body must include all required fields (e.g., user, gold_amount, status) even if some fields remain unchanged. '
        'The gold_amount must be non-negative, and status must be one of ACCEPTED, WAITING, or REJECTED. '
        'The response returns the updated request’s details. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.gold_withdrawal_request'],
    request_body=GoldWithdrawalRequestSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the gold withdrawal request to update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: GoldWithdrawalRequestSerializer,
        400: 'Invalid input data (e.g., negative amount or invalid status).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Gold withdrawal request with the specified ID does not exist.'
    }
)

admin_partial_update_gold_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='Partially Update a Gold Withdrawal Request (Admin)',
    operation_description=(
        'This endpoint allows administrators to partially update the details of an existing gold withdrawal request identified by its ID. '
        'Only the provided fields in the request body will be updated (e.g., updating only gold_amount or status). '
        'The gold_amount must be non-negative, and status must be one of ACCEPTED, WAITING, or REJECTED. '
        'The response returns the updated request’s details. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.gold_withdrawal_request'],
    request_body=GoldWithdrawalRequestSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the gold withdrawal request to partially update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: GoldWithdrawalRequestSerializer,
        400: 'Invalid input data (e.g., negative amount or invalid status).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Gold withdrawal request with the specified ID does not exist.'
    }
)

admin_destroy_gold_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='Delete a Gold Withdrawal Request (Admin)',
    operation_description=(
        'This endpoint allows administrators to delete a gold withdrawal request by its ID. '
        'The operation permanently removes the request from the system. '
        'A successful deletion returns a 204 No Content response. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.gold_withdrawal_request'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the gold withdrawal request to delete.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        204: 'Gold withdrawal request successfully deleted.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Gold withdrawal request with the specified ID does not exist.'
    }
)

admin_list_gold_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='List All Gold Withdrawal Requests (Admin)',
    operation_description=(
        'This endpoint allows administrators to retrieve a list of all gold withdrawal request records in the system. '
        'The response includes details for each request, such as ID, associated user, create_date, gold_amount, status, and status display. '
        'Optional search functionality is available using the "search" query parameter to filter requests by username or status. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.gold_online_store.gold_withdrawal_request'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter requests by username or status (partial match).", type=openapi.TYPE_STRING)
    ],
    responses={
        200: GoldWithdrawalRequestSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

# GoldWithdrawalRequestAPIView Decorators
user_create_gold_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='Create a New Gold Withdrawal Request (User)',
    operation_description=(
        'This endpoint allows authenticated users to create a new gold withdrawal request for themselves. '
        'The request must include gold_amount and status (ACCEPTED, WAITING, or REJECTED). '
        'The gold_amount must be non-negative and within reasonable limits. '
        'The create_date is automatically set to the current time if not provided. '
        'The user field is automatically set to the authenticated user and cannot be modified. '
        'The response returns the created request’s details, including status display. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.gold_withdrawal_request'],
    request_body=GoldWithdrawalRequestSerializer,
    responses={
        201: GoldWithdrawalRequestSerializer,
        400: 'Invalid input data (e.g., negative amount or invalid status).',
        401: 'Unauthorized: Valid JWT token required.'
    }
)

user_retrieve_gold_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='Retrieve Own Gold Withdrawal Request Details',
    operation_description=(
        'This endpoint allows authenticated users to retrieve their own gold withdrawal request information by its ID. '
        'The response includes details such as ID, associated user, create_date, gold_amount, status, and status display. '
        'The request ID must correspond to a request belonging to the authenticated user, and users cannot access other users’ requests. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.gold_withdrawal_request'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s gold withdrawal request.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: GoldWithdrawalRequestSerializer,
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only access their own gold withdrawal request.',
        404: 'Not Found: Gold withdrawal request with the specified ID does not exist.'
    }
)

user_update_gold_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='Fully Update Own Gold Withdrawal Request',
    operation_description=(
        'This endpoint allows authenticated users to fully update their own gold withdrawal request identified by its ID. '
        'The request body must include all required fields (e.g., gold_amount, status) even if some fields remain unchanged. '
        'The gold_amount must be non-negative, and status must be one of ACCEPTED, WAITING, or REJECTED. '
        'The user field cannot be modified and must match the authenticated user. '
        'The response returns the updated request’s details. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.gold_withdrawal_request'],
    request_body=GoldWithdrawalRequestSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s gold withdrawal request to update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: GoldWithdrawalRequestSerializer,
        400: 'Invalid input data (e.g., negative amount or invalid status).',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only update their own gold withdrawal request.',
        404: 'Not Found: Gold withdrawal request with the specified ID does not exist.'
    }
)

user_partial_update_gold_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='Partially Update Own Gold Withdrawal Request',
    operation_description=(
        'This endpoint allows authenticated users to partially update their own gold withdrawal request identified by its ID. '
        'Only the provided fields in the request body will be updated (e.g., updating only gold_amount or status). '
        'The gold_amount must be non-negative, and status must be one of ACCEPTED, WAITING, or REJECTED. '
        'The user field cannot be modified and must match the authenticated user. '
        'The response returns the updated request’s details. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.gold_withdrawal_request'],
    request_body=GoldWithdrawalRequestSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s gold withdrawal request to partially update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: GoldWithdrawalRequestSerializer,
        400: 'Invalid input data (e.g., negative amount or invalid status).',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only update their own gold withdrawal request.',
        404: 'Not Found: Gold withdrawal request with the specified ID does not exist.'
    }
)

user_destroy_gold_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='Delete Own Gold Withdrawal Request',
    operation_description=(
        'This endpoint allows authenticated users to delete their own gold withdrawal request by its ID. '
        'The operation permanently removes the request from the system. '
        'The request ID must correspond to a request belonging to the authenticated user. '
        'A successful deletion returns a 204 No Content response. '
        'This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.gold_withdrawal_request'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user’s gold withdrawal request to delete.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        204: 'Gold withdrawal request successfully deleted.',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only delete their own gold withdrawal request.',
        404: 'Not Found: Gold withdrawal request with the specified ID does not exist.'
    }
)

user_list_gold_withdrawal_request_swagger = swagger_auto_schema(
    operation_summary='List Own Gold Withdrawal Requests',
    operation_description=(
        'This endpoint allows authenticated users to retrieve a list of their own gold withdrawal request records. '
        'The response includes details for each request, such as ID, associated user, create_date, gold_amount, status, and status display. '
        'Optional search functionality is available using the "search" query parameter to filter requests by status. '
        'Users can only access their own requests. This operation requires JWT authentication.'
    ),
    tags=['gold_online_store.gold_withdrawal_request'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter requests by status (partial match).", type=openapi.TYPE_STRING)
    ],
    responses={
        200: GoldWithdrawalRequestSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only access their own gold withdrawal requests.'
    }
)