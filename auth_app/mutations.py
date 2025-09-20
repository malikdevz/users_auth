import graphene
import graphql_jwt
import datetime
from .types import *
from .models import *
from django.contrib.auth.models import User
from .tools import *
from graphql import GraphQLError
import jwt
from django.conf import settings
from graphql_jwt.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
import random, string
from datetime import timedelta
from django.utils import timezone




#une fonction utilitaire pour envoyer le mail--------------------------------------------------------------
def send_verification_code(user, title="ICARTABLE!"):
    # Générer un code à 6 chiffres
    code = ''.join(random.choices(string.digits, k=6))
    expires_at = timezone.now() + timedelta(minutes=10)  # expire après 10 min

    VerificationCode.objects.create(user=user, code=code, expires_at=expires_at)

    send_mail(title,f"Votre code de confirmation est (expire dans 10 minutes) : {code}.",settings.EMAIL_HOST_USER,[user.email],fail_silently=False)
#----------------------------------------------------------------------------------------------------------

#Generer et envoyer un code de verification a l'utilisateur par email--------------------------------------------
class SendConfirmCode(graphene.Mutation):

	class Arguments:
		email_title=graphene.String(required=True)
		user_password=graphene.String(required=True)

	is_code_send=graphene.Boolean()

	@login_required
	def mutate(root,info, email_title, user_password):
		user=info.context.user
		if not check_password(user_password, user.password):
			raise GraphQLError("INVALID_PASSWORD")
		else:
			#envoyer le code de verification a l'utilisateur
			if not user.email:
				raise GraphQLError("USER_EMAIL_EMPTY") 
			send_verification_code(user, title=email_title)
			return SendConfirmCode(is_code_send=True)
#---------------------------------------------------------------------------------------------------------------


#Creer un compte de login, cette requete est destine a l'API USer manager-----------------------------------
class CreateUserLogin(graphene.Mutation):

	class Arguments:
		username=graphene.String(required=True)
		password=graphene.String(required=True)
		email=graphene.String(required=False)

	user_login=graphene.Field(UserType)

	def mutate(root, info, username, password, email=None):
		if username and password:
			user_data={
			"username":username,
			"password":password,
			"is_superuser":False,
			"is_staff":False
			}
			if email:
				if is_valid_email(email):
					user_data['email']=email
					if User.objects.filter(email=email).exists():
						raise GraphQLError("EMAIL_ALREAD_EXIST")

				else:
					raise GraphQLError("EMAIL_INVALID")
			if User.objects.filter(username=username).exists():
				raise GraphQLError("USERNAME_ALREAD_EXIST")
			user=User.objects.create_user(**user_data)
			return CreateUserLogin(user_login=user)
		else:
			raise GraphQLError("EMPY_FIELD_ERROR")
#----------------------------------------------------------------------------------------------------------------

#Verifier le compte
class VerifyUserAccount(graphene.Mutation):

	class Arguments:
		verification_code=graphene.String(required=True)

	account_is_verified=graphene.Boolean()

	@login_required
	def mutate(root, info, verification_code):
		user=info.context.user
		try:
			vc = VerificationCode.objects.filter(user=user, code=verification_code).latest('created_at')
		except VerificationCode.DoesNotExist:
			raise GraphQLError("VERIFICATION_CODE_INVALID")

		if not vc.is_valid():
			raise GraphQLError("VERIFICATION_CODE_EXPIRED")
		else:
			#here we call Account Manager Api to verify and update user account
			pass 

		return VerifyUserAccount(account_is_verified=True)	


#Changer le mot de passe de l'utilisateur------------------------------------------------------------------------
class ChangePassword(graphene.Mutation):

	class Arguments:
		verification_code=graphene.String(required=True)
		new_password=graphene.String(required=True)

	is_password_changed=graphene.Boolean()

	@login_required
	def mutate(root,info, verification_code, new_password):
		user=info.context.user
		try:
			vc = VerificationCode.objects.filter(user=user, code=verification_code).latest('created_at')
		except VerificationCode.DoesNotExist:
			raise GraphQLError("VERIFICATION_CODE_INVALID")
		if not vc.is_valid():
			raise GraphQLError("VERIFICATION_CODE_EXPIRED")

		if len(new_password) < 6:
			raise GraphQLError("PASSWORD_IS_TO_SHORT")
		user.set_password(new_password)
		user.save()
		vc.delete()
		return ChangePassword(is_password_changed=True)
#----------------------------------------------------------------------------------------------------------------

#Make a teacher an admin- plus de controle du cote de account manager
class GiveAdminAccess(graphene.Mutation):

	class Arguments:
		user_username=graphene.String(required=True)

	is_give_access_success=graphene.Boolean()

	@login_required
	def mutate(root, info, user_username):
		user=info.context.user
		if user.is_superuser:#seul un admin  peu accourder les acces admin aux professeur
			if User.objects.filter(username=user_username).exists():
				n_user=User.objects.get(username=user_username)
				n_user.is_superuser=True
				n_user.save()
				return GiveAdminAccess(is_give_access_success=True)
			else:
				raise GraphQLError("USER_NOT_EXIST")
		else:
			raise GraphQLError("OPERATION_DENIED")

#Revoke admin access
class RevokeAdminAccess(graphene.Mutation):

	class Arguments:
		user_username=graphene.String(required=True)

	is_revoke_access_success=graphene.Boolean()

	@login_required
	def mutate(root, info, user_username):
		user=info.context.user
		if user.is_superuser:#seul un admin  peu accourder les acces admin aux professeur
			if User.objects.filter(username=user_username).exists():
				n_user=User.objects.get(username=user_username)
				n_user.is_superuser=False
				n_user.save()
				return GiveAdminAccess(is_give_access_success=True)
			else:
				raise GraphQLError("USER_NOT_EXIST")
		else:
			raise GraphQLError("OPERATION_DENIED")





#Le professeur peu reinitialiser le mot de passe de ses eleves-----------------------------------
class ResetStudentPassword(graphene.Mutation):

	class Arguments:
		student_username=graphene.String(required=True)

	is_password_reset=graphene.Boolean()

	@login_required
	def mutate(root, info, student_username):
		user=info.context.user
		#ici requette pour recuperer le compte utilisateur du professeur, verifier s'il est prof et si cette 
		#eleve fait parti de l'une de ses classe
		#
		#--------Code a remplir plus tard donc!------------------------------------------------

		return ResetStudentPassword(is_password_reset=True)


#--------------------------------------------------------------------------------------------------


#Le professeur peu supprimer le compte de ses eleves----------------------------------------------
class DeleteStudentAccount(graphene.Mutation):

	class Arguments:
		pass
	is_account_deleted=graphene.Boolean()

	@login_required
	def mutate(root, info):
		user=info.context.user
		#ici requette pour recuperer le compte utilisateur du professeur, verifier s'il est prof et si cette 
		#eleve fait parti de l'une de ses classe
		#
		#--------Code a remplir plus tard donc!-----------------------------------------------
		return DeleteMyAccount(is_account_deleted=True)
#-------------------------------------------------------------------------------


#Supprimer le compte utilisateur---------------------------------------------------------------------------
class DeleteUserAccount(graphene.Mutation):

	class Arguments:
		verification_code=graphene.String(required=True)

	is_accound_deleted=graphene.Boolean()

	@login_required
	def mutate(root,info, verification_code):
		user=info.context.user
		try:
			vc = VerificationCode.objects.filter(user=user, code=verification_code).latest('created_at')
		except VerificationCode.DoesNotExist:
			raise GraphQLError("VERIFICATION_CODE_INVALID")
		if not vc.is_valid():
			raise GraphQLError("VERIFICATION_CODE_EXPIRED")

		user.delete()
		vc.delete()
		return DeleteUserAccount(is_accound_deleted=True)
#---------------------------------------------------------------------------------------------------------------


#Un administrateur peut supprimer n'importe quelle compte-------------------------------------------------------
class DeleteAnyAccount(graphene.Mutation):

	class Arguments:
		username=graphene.String(required=True)

	is_account_deleted=graphene.Boolean()

	@login_required
	def mutate(root, info, username):
		user=info.context.user
		if not user.is_superuser:
			raise GraphQLError(f"OPERATION_DENIED-{user.username}")
		else:
			if not User.objects.filter(username=username).exists():
				raise GraphQLError("USER_NOT_EXIST")
			else:
				User.objects.get(username=username).delete()
				return DeleteAnyAccount(is_account_deleted=True)
#-------------------------------------------------------------------------------------------------------------------



class Mutation(graphene.ObjectType):
	create_user_login=CreateUserLogin.Field()#OK
	verify_user_account=VerifyUserAccount.Field()
	change_password=ChangePassword.Field()
	send_confirm_code=SendConfirmCode.Field()
	delete_user_account=DeleteUserAccount.Field()
	admin_delete_account=DeleteAnyAccount.Field()
	give_admin_access=GiveAdminAccess.Field()
	revoke_admin_access=RevokeAdminAccess.Field()

	#Token manager------------------------
	token_auth = graphql_jwt.ObtainJSONWebToken.Field()#OK
	verify_token = graphql_jwt.Verify.Field()
	refresh_token = graphql_jwt.Refresh.Field()
	#------------------------------