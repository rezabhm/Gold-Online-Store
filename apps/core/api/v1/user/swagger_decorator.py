from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.core.serializers import CustomUserSerializer

# UserAdminAPIView Decorators
admin_create_user_swagger = swagger_auto_schema(
    operation_summary='Create a New User (Admin)',
    operation_description=(
        'This endpoint allows administrators to create a new user account in the system. '
        'The request must include user details such as username, email, user_role (admin or customer), '
        'first_name, and last_name. The user_role must be either "admin" or "customer". '
        'The response returns the created user’s details, including the automatically generated ID and is_active status. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.user'],
    request_body=CustomUserSerializer,
    responses={
        201: CustomUserSerializer,
        400: 'Invalid input data (e.g., missing required fields or invalid user_role).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_retrieve_user_swagger = swagger_auto_schema(
    operation_summary='Retrieve User Details (Admin)',
    operation_description=(
        'This endpoint allows administrators to retrieve detailed information about a specific user by their ID. '
        'The response includes user details such as ID, username, email, user_role, first_name, last_name, and is_active status. '
        'This operation is restricted to admin users only and requires JWT authentication. '
        'The user ID must be provided in the URL path.'
    ),
    tags=['admin.core.user'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the user to retrieve.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: CustomUserSerializer,
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: User with the specified ID does not exist.'
    }
)

admin_update_user_swagger = swagger_auto_schema(
    operation_summary='Fully Update a User (Admin)',
    operation_description=(
        'This endpoint allows administrators to fully update the details of an existing user identified by their ID. '
        'The request body must include all required fields (e.g., username, email, user_role) even if some fields remain unchanged. '
        'The user_role must be either "admin" or "customer". '
        'The response returns the updated user’s details. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.user'],
    request_body=CustomUserSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the user to update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: CustomUserSerializer,
        400: 'Invalid input data (e.g., missing required fields or invalid user_role).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: User with the specified ID does not exist.'
    }
)

admin_partial_update_user_swagger = swagger_auto_schema(
    operation_summary='Partially Update a User (Admin)',
    operation_description=(
        'This endpoint allows administrators to partially update the details of an existing user identified by their ID. '
        'Unlike full update, only the provided fields in the request body will be updated (e.g., updating only email or user_role). '
        'The user_role must be either "admin" or "customer". '
        'The response returns the updated user’s details. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.user'],
    request_body=CustomUserSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the user to partially update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: CustomUserSerializer,
        400: 'Invalid input data (e.g., invalid user_role).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: User with the specified ID does not exist.'
    }
)

admin_destroy_user_swagger = swagger_auto_schema(
    operation_summary='Delete a User (Admin)',
    operation_description=(
        'This endpoint allows administrators to delete a user account by their ID. '
        'The operation permanently removes the user from the system. '
        'A successful deletion returns a 204 No Content response. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.user'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the user to delete.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        204: 'User successfully deleted.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: User with the specified ID does not exist.'
    }
)

admin_list_user_swagger = swagger_auto_schema(
    operation_summary='List All Users (Admin)',
    operation_description=(
        'This endpoint allows administrators to retrieve a list of all user records in the system. '
        'The response includes details for each user, such as ID, username, email, user_role, first_name, last_name, and is_active status. '
        'Optional search functionality is available using the "search" query parameter to filter users by username or email. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.user'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter users by username or email (partial match).", type=openapi.TYPE_STRING)
    ],
    responses={
        200: CustomUserSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

# UserAPIView Decorators
user_retrieve_user_swagger = swagger_auto_schema(
    operation_summary='Retrieve Own User Details',
    operation_description=(
        'This endpoint allows authenticated users to retrieve their own user information by their ID. '
        'The response includes details such as ID, username, email, user_role, first_name, last_name, and is_active status. '
        'The user can only access their own record, and the ID in the URL must match the authenticated user’s ID. '
        'This operation requires JWT authentication.'
    ),
    tags=['core.user'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: CustomUserSerializer,
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only access their own record.',
        404: 'Not Found: User with the specified ID does not exist.'
    }
)

user_update_user_swagger = swagger_auto_schema(
    operation_summary='Fully Update Own User Record',
    operation_description=(
        'This endpoint allows authenticated users to fully update their own user information by their ID. '
        'The request body must include all required fields (e.g., username, email, user_role), even if some fields remain unchanged. '
        'The user_role must be either "admin" or "customer", but non-admin users cannot change their role to "admin". '
        'The ID in the URL must match the authenticated user’s ID. '
        'This operation requires JWT authentication.'
    ),
    tags=['core.user'],
    request_body=CustomUserSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: CustomUserSerializer,
        400: 'Invalid input data (e.g., missing required fields or invalid user_role).',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only update their own record or attempted to change user_role to admin.',
        404: 'Not Found: User with the specified ID does not exist.'
    }
)

user_partial_update_user_swagger = swagger_auto_schema(
    operation_summary='Partially Update Own User Record',
    operation_description=(
        'This endpoint allows authenticated users to partially update their own user information by their ID. '
        'Only the provided fields in the request body will be updated (e.g., updating only email or first_name). '
        'The user_role must be either "admin" or "customer", but non-admin users cannot change their role to "admin". '
        'The ID in the URL must match the authenticated user’s ID. '
        'This operation requires JWT authentication.'
    ),
    tags=['core.user'],
    request_body=CustomUserSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the authenticated user.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: CustomUserSerializer,
        400: 'Invalid input data (e.g., invalid user_role).',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only update their own record or attempted to change user_role to admin.',
        404: 'Not Found: User with the specified ID does not exist.'
    }
)

# UserRegisterAPIView Decorators
register_create_user_swagger = swagger_auto_schema(
    operation_summary='Register a New User',
    operation_description=(
        'This endpoint allows unauthenticated users to register a new user account in the system. '
        'The request must include user details such as username, email, user_role (must be "customer"), '
        'first_name, and last_name. The user_role for new registrations is restricted to "customer" to prevent '
        'unauthenticated users from creating admin accounts. '
        'The response returns the created user’s details, including the automatically generated ID and is_active status. '
        'No authentication is required for this endpoint.'
    ),
    tags=['core.user'],
    request_body=CustomUserSerializer,
    responses={
        201: CustomUserSerializer,
        400: 'Invalid input data (e.g., missing required fields, invalid user_role, or duplicate username/email).'
    }
)