from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from .models import Book,Profile
from .forms import BookForm, SignupForm, LoginForm
from .forms import ProfileForm
from django.contrib import messages

# Create your views here.
def index(request):
  q = (request.GET.get('q') or "").strip()

  books = Book.objects.all()
  if q:
     isnum = q.isdigit()
     books = books.filter(
            Q(title__icontains=q) |
            Q(author__icontains=q) |
            Q(notes__icontains=q) |
            Q(gener__icontains=q) |
            (Q(rating=int(q)) if isnum else Q(pk=None))
        )
  context = {
        "books": books,
        "q": q,
    }

  return render(request, 'book/index.html', context)
@login_required
def addBook(request):
  GENRES = [
        "Fiction",  "Non-fiction", "Sci-Fi",
        "Fantasy",  "Biography",  "Other",
    ]
  if request.method == "POST":
    title = request.POST.get("title")
    author=request.POST.get("author")
    gener=request.POST.get("gener")
    rating=request.POST.get("rating")
    notes=request.POST.get("notes")
    book=Book(title=title,author=author,gener=gener,rating=rating,notes=notes)
    book.owner = request.user
    book.save()
    return redirect('index')

  ratings = range(0,11)
  return render(request, 'book/addbook.html', {'GENERS': GENRES, 'ratings': ratings})


def bookDetail(request,id):
  book = get_object_or_404(Book, pk=id)
  return render(request, 'book/bookdetail.html',{'book':book})

def recentlyAdded(request):
  recentAdded = Book.objects.all().order_by('-created_at')[:5]  # limit to last 5
  return render(request, 'book/recentlyAdded.html', {'recentAdded': recentAdded})

@login_required
def editBook(request, id):
    book = get_object_or_404(Book, pk=id)
    if book.owner and book.owner != request.user:
        
        messages.error(request, "You can only edit books you added.")
        return redirect("index")  # or redirect("bookDetail", id=id)

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated.")
            return redirect("index")
    else:
        form = BookForm(instance=book)
    return render(request, "book/editBook.html", {"form": form, "book": book})

@require_POST
@login_required
def deleteBook(request, id):
    book = get_object_or_404(Book, pk=id)
    if book.owner and book.owner != request.user:
        # was: raise PermissionDenied("Not your book, So you can't delete!")
        messages.error(request, "You can only delete books you added.")
        return redirect("index")  # or redirect("bookDetail", id=id)
    title = book.title
    book.delete()
    messages.success(request, f'Deleted “{title}”.')
    return redirect("index")

def search_suggest(request):
    q = (request.GET.get("q") or "").strip()
    if not q:
        return JsonResponse({"results": []})

    qs = (Book.objects
          .filter(Q(title__icontains=q) | Q(author__icontains=q))
          .order_by('-created_at')
          .values('id', 'title', 'author')[:8])  # top 8

    # Return lightweight list
    results = [{"id": b["id"], "label": f'{b["title"]} — {b["author"]}'} for b in qs]
    return JsonResponse({"results": results})

@login_required
def my_books(request):
    q = request.GET.get("q", "").strip()
    books = Book.objects.filter(owner=request.user).order_by("-created_at")
    if q:
        books = books.filter(Q(title__icontains=q) | Q(author__icontains=q))
    return render(request, "book/my_books.html", {"books": books, "q": q})

# ---------- Auth ----------
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Account created.")
            return redirect("index")
    else:
        form = SignupForm()
    return render(request, "book/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Logged in.")
            return redirect("index")
    else:
        form = LoginForm(request)
    return render(request, "book/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out.")
    return redirect("index")

# ---------- Profiles ----------
@login_required
def profile_me(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile_me")  # back to the same page in view mode
    else:
        form = ProfileForm(instance=profile)

    recent_books = Book.objects.filter(owner=request.user).order_by("-created_at")[:6]
    count = Book.objects.filter(owner=request.user).count()

    # Optional: open the edit form by default if ?edit=1 is present
    start_in_edit = request.GET.get("edit") == "1"

    return render(
        request,
        "book/profile_me.html",
        {
            "profile": profile,
            "form": form,
            "user_obj": request.user,
            "recent_books": recent_books,
            "count": count,
            "start_in_edit": start_in_edit,
        },
    )
def profile_user(request, username):
    user_obj = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=user_obj)
    count = Book.objects.filter(owner=user_obj).count()

    # Permissions: owner or admin can see private bits
    can_view_private = request.user.is_authenticated and (
        request.user == user_obj or request.user.is_staff or request.user.is_superuser
    )

    recent_books = Book.objects.filter(owner=user_obj).order_by("-created_at")[:6]
    return render(
        request,
        "book/profile_public.html",
        {
            "profile": profile,
            "user_obj": user_obj,
            "count": count,
            "recent_books": recent_books,
            "can_view_private": can_view_private,
        },
    )
