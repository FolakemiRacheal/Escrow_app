from django.shortcuts import render

# Create your views here.
def account(request):
    return render(request, 'ums/home.html')


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LoginView(generics.GenericsAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowyAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data("username")
        password = serializer.validated_data("password")


        user = authenticate(request, username=username, password=password)

        if user is not None:
            return Resonse(
                {"detail":"Incorrect login details"}
            )

            refresh = RefreshToken.for_user(user)

            return Response(
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            )

