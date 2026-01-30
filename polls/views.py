from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from .models import Poll, Choice, Vote
from .forms import PollForm, ChoiceFormSet
from prometheus_client import Counter

votes_cast_total = Counter("votes_cast_total", "Total number of votes cast")


class PollListView(ListView):
    model = Poll
    template_name = "polls/poll_list.html"
    context_object_name = "polls"
    paginate_by = 10

    def get_queryset(self):
        return (
            Poll.objects.filter(is_active=True, choices__isnull=False)
            .distinct()
            .order_by("-created_at")
        )


class PollDetailView(DetailView):
    model = Poll
    template_name = "polls/poll_detail.html"
    context_object_name = "poll"


class PollCreateView(LoginRequiredMixin, CreateView):
    model = Poll
    form_class = PollForm
    template_name = "polls/poll_form.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["choice_formset"] = ChoiceFormSet(self.request.POST)
        else:
            data["choice_formset"] = ChoiceFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        choice_formset = context["choice_formset"]

        if form.is_valid() and choice_formset.is_valid():
            form.instance.creator = self.request.user
            self.object = form.save()
            choice_formset.instance = self.object
            choice_formset.save()
            messages.success(self.request, "Poll created successfully!")
            return redirect(self.object.get_absolute_url())
        else:
            if not form.is_valid():
                messages.error(self.request, "There were errors in the poll details.")
            if not choice_formset.is_valid():
                messages.error(
                    self.request,
                    "There were errors in the poll choices. "
                    "Ensure you have at least 2 choices.",
                )
            return self.render_to_response(
                self.get_context_data(form=form, choice_formset=choice_formset)
            )


class PollUpdateView(LoginRequiredMixin, UpdateView):
    model = Poll
    form_class = PollForm
    template_name = "polls/poll_form.html"

    def dispatch(self, request, *args, **kwargs):
        poll = self.get_object()
        if poll.creator != request.user and not request.user.is_staff:
            messages.error(request, "You do not have permission to edit this poll.")
            return redirect("polls:poll_detail", slug=poll.slug)

        if poll.votes.exists() and not request.user.is_staff:
            messages.error(request, "Cannot edit poll after voting has started.")
            return redirect("polls:poll_results", slug=poll.slug)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["choice_formset"] = ChoiceFormSet(
                self.request.POST, instance=self.object
            )
        else:
            if "choice_formset" not in data:
                data["choice_formset"] = ChoiceFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        choice_formset = context["choice_formset"]

        if form.is_valid() and choice_formset.is_valid():
            self.object = form.save()
            choice_formset.instance = self.object
            choice_formset.save()
            messages.success(self.request, "Poll updated successfully!")
            return redirect(self.object.get_absolute_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=form, choice_formset=choice_formset)
            )


class PollDeleteView(LoginRequiredMixin, View):
    def post(self, request, slug):
        poll = get_object_or_404(Poll, slug=slug)
        if poll.creator != request.user and not request.user.is_staff:
            messages.error(request, "You do not have permission to delete this poll.")
            return redirect("polls:poll_list")

        # Hard delete
        poll.delete()
        messages.success(request, "Poll deleted permanently.")
        return redirect("polls:poll_list")


class VoteView(View):
    def post(self, request, slug):
        poll = get_object_or_404(Poll, slug=slug)
        choice_id = request.POST.get("choice")

        if not choice_id:
            messages.error(request, "No choice selected.")
            return redirect("polls:poll_detail", slug=slug)

        choice = get_object_or_404(Choice, id=choice_id, poll=poll)

        # Check if poll is active
        if not poll.is_active or poll.is_archived:
            messages.error(request, "This poll is no longer active.")
            return redirect("polls:poll_list")

        # Check if poll has ended
        if poll.end_date and poll.end_date < timezone.now():
            messages.error(request, "This poll has ended.")
            return redirect("polls:poll_results", slug=slug)

        # Handle user voting
        user = request.user if request.user.is_authenticated else None
        ip = request.META.get("REMOTE_ADDR")

        if user:
            # Check if user already voted
            if (
                not poll.allow_multiple_votes
                and Vote.objects.filter(poll=poll, user=user).exists()
            ):
                messages.error(request, "You have already voted in this poll.")
                return redirect("polls:poll_results", slug=slug)
        else:
            # Anonymous voting check
            if not poll.is_public:
                messages.error(request, "Please login to vote in this private poll.")
                return redirect("users:login")

            # Use IP to check for duplicate anonymous votes
            if (
                not poll.allow_multiple_votes
                and Vote.objects.filter(
                    poll=poll, user__isnull=True, ip_address=ip
                ).exists()
            ):
                messages.error(
                    request, "Someone from your IP has already voted anonymously."
                )
                return redirect("polls:poll_results", slug=slug)

        Vote.objects.create(
            poll=poll,
            choice=choice,
            user=user,
            ip_address=ip,
            user_agent=request.META.get("HTTP_USER_AGENT"),
        )
        votes_cast_total.inc()
        messages.success(request, f"Vote recorded for '{choice.choice_text}'!")
        return redirect("polls:poll_results", slug=slug)


class PollResultsView(DetailView):
    model = Poll
    template_name = "polls/poll_results.html"
    context_object_name = "poll"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poll = self.get_object()
        choices = poll.choices.annotate(vote_count=Count("votes"))
        total_votes = sum(c.vote_count for c in choices)

        for choice in choices:
            if total_votes > 0:
                choice.percentage = (choice.vote_count / total_votes) * 100
            else:
                choice.percentage = 0

        context["choices"] = choices
        context["total_votes"] = total_votes
        return context
