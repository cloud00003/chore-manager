from datetime import date, datetime, timezone as datetime_timezone
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Chore


class ChoreOverdueTests(TestCase):
    @patch("chores.models.timezone.localdate", return_value=date(2026, 9, 10))
    def test_overdue_boundaries_and_labels(self, localdate):
        for deadline, completed, expected in (
            (date(2026, 9, 9), False, True),
            (date(2026, 9, 10), False, False),
            (date(2026, 9, 11), False, False),
            (date(2026, 9, 9), True, False),
        ):
            with self.subTest(deadline=deadline, completed=completed):
                chore = Chore.objects.create(
                    title="Wash dishes", responsible_person="Alex",
                    deadline=deadline, is_completed=completed,
                )
                self.assertEqual(chore.is_overdue, expected)
                response = self.client.get(reverse("chores:chore_list"))
                self.assertContains(response, "Overdue", count=int(expected))
                chore.delete()

    @patch("django.utils.timezone.now")
    def test_overdue_uses_local_date(self, now):
        now.return_value = datetime(2026, 9, 9, 20, tzinfo=datetime_timezone.utc)
        chore = Chore(deadline=date(2026, 9, 9))
        with timezone.override("Asia/Almaty"):
            self.assertTrue(chore.is_overdue)
        with timezone.override("UTC"):
            self.assertFalse(chore.is_overdue)


class ChoreCompleteTests(TestCase):
    def setUp(self):
        self.chore = Chore.objects.create(
            title="Wash dishes", responsible_person="Alex",
            deadline=date(2020, 1, 1),
        )
        self.url = reverse("chores:chore_complete", args=[self.chore.pk])

    def test_completion_moves_chore_and_removes_overdue_label(self):
        response = self.client.get(reverse("chores:chore_list"))
        self.assertContains(response, "Overdue")
        self.assertContains(response, f'action="{self.url}"')

        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, reverse("chores:chore_list"))
        self.chore.refresh_from_db()
        self.assertTrue(self.chore.is_completed)
        self.assertEqual(self.chore.title, "Wash dishes")
        self.assertEqual(self.chore.responsible_person, "Alex")
        self.assertEqual(self.chore.deadline, date(2020, 1, 1))
        self.assertQuerySetEqual(response.context["incomplete_chores"], [])
        self.assertQuerySetEqual(response.context["completed_chores"], [self.chore])
        self.assertContains(response, "Wash dishes")
        self.assertContains(response, "No incomplete chores.")
        self.assertNotContains(response, "Overdue")
        self.assertNotContains(response, "Mark as completed")

    def test_get_cannot_complete_chore(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.chore.refresh_from_db()
        self.assertFalse(self.chore.is_completed)

    def test_missing_chore_returns_404(self):
        self.chore.delete()
        self.assertEqual(self.client.post(self.url).status_code, 404)

    def test_repeated_completion_keeps_chore_completed(self):
        self.client.post(self.url)
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("chores:chore_list"))
        self.chore.refresh_from_db()
        self.assertTrue(self.chore.is_completed)
        self.assertEqual(Chore.objects.count(), 1)

    def test_completion_requires_rendered_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(self.url)
        self.assertEqual(response.status_code, 403)
        self.chore.refresh_from_db()
        self.assertFalse(self.chore.is_completed)

        response = client.get(reverse("chores:chore_list"))
        from html.parser import HTMLParser

        class TokenParser(HTMLParser):
            token = None

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if tag == "input" and attrs.get("name") == "csrfmiddlewaretoken":
                    self.token = attrs.get("value")

        parser = TokenParser()
        parser.feed(response.content.decode())
        self.assertTrue(parser.token)
        response = client.post(self.url, {"csrfmiddlewaretoken": parser.token})
        self.assertRedirects(response, reverse("chores:chore_list"))
        self.chore.refresh_from_db()
        self.assertTrue(self.chore.is_completed)


class ChoreModelTests(TestCase):
    def test_chore_fields_and_default_are_persisted(self):
        chore = Chore.objects.create(
            title="Wash the dishes",
            responsible_person="Alex",
            deadline=date(2026, 9, 10),
        )

        saved_chore = Chore.objects.get(pk=chore.pk)

        self.assertEqual(saved_chore.title, "Wash the dishes")
        self.assertEqual(saved_chore.responsible_person, "Alex")
        self.assertEqual(saved_chore.deadline, date(2026, 9, 10))
        self.assertFalse(saved_chore.is_completed)

    def test_required_fields_are_validated(self):
        for field, empty_value in (
            ("title", ""),
            ("responsible_person", ""),
            ("deadline", None),
        ):
            with self.subTest(field=field):
                chore = Chore(
                    title="Wash the dishes",
                    responsible_person="Alex",
                    deadline=date(2026, 9, 10),
                )
                setattr(chore, field, empty_value)

                with self.assertRaises(ValidationError) as error:
                    chore.full_clean()

                self.assertIn(field, error.exception.message_dict)


class ChoreListTests(TestCase):
    def test_empty_list_at_home_page(self):
        self.assertEqual(reverse("chores:chore_list"), "/")
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chores/chore_list.html")
        self.assertContains(response, "Incomplete")
        self.assertContains(response, "Completed")
        self.assertContains(response, "No incomplete chores.")
        self.assertContains(response, "No completed chores yet.")

    def test_chores_render_in_the_correct_sections(self):
        Chore.objects.create(
            title="Wash dishes",
            responsible_person="Alex",
            deadline=date(2026, 9, 10),
        )
        Chore.objects.create(
            title="Sweep floor",
            responsible_person="Sam",
            deadline=date(2026, 9, 9),
            is_completed=True,
        )

        response = self.client.get(reverse("chores:chore_list"))
        self.assertEqual(response.status_code, 200)
        page = response.content.decode()
        incomplete = page.split('<section aria-labelledby="incomplete-heading">')[
            1
        ].split("</section>")[0]
        completed = page.split('<section aria-labelledby="completed-heading">')[
            1
        ].split("</section>")[0]

        for value in ("Wash dishes", "Alex", "2026-09-10"):
            self.assertIn(value, incomplete)
            self.assertNotIn(value, completed)
        for value in ("Sweep floor", "Sam", "2026-09-09"):
            self.assertIn(value, completed)
            self.assertNotIn(value, incomplete)
        self.assertNotContains(response, "No incomplete chores.")
        self.assertNotContains(response, "No completed chores yet.")

    def test_each_section_has_an_independent_empty_state(self):
        for is_completed in (False, True):
            with self.subTest(is_completed=is_completed):
                chore = Chore.objects.create(
                    title="Wash dishes",
                    responsible_person="Alex",
                    deadline=date(2026, 9, 10),
                    is_completed=is_completed,
                )
                response = self.client.get(reverse("chores:chore_list"))
                if is_completed:
                    self.assertContains(response, "No incomplete chores.")
                    self.assertNotContains(response, "No completed chores yet.")
                else:
                    self.assertNotContains(response, "No incomplete chores.")
                    self.assertContains(response, "No completed chores yet.")
                chore.delete()


class ChoreCreateTests(TestCase):
    def setUp(self):
        self.url = reverse("chores:chore_create")
        self.valid_data = {
            "title": "Wash dishes",
            "responsible_person": "Alex",
            "deadline": "2026-09-10",
        }

    def test_list_links_to_create_page_and_get_does_not_save(self):
        response = self.client.get(reverse("chores:chore_list"))
        self.assertContains(response, f'href="{self.url}"')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chores/chore_form.html")
        for field in self.valid_data:
            self.assertContains(response, f'name="{field}"')
        self.assertContains(response, 'type="date"')
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertNotContains(response, 'name="is_completed"')
        self.assertEqual(Chore.objects.count(), 0)

    def test_valid_submission_creates_incomplete_chore_and_redirects(self):
        response = self.client.post(
            self.url, {**self.valid_data, "is_completed": "true"}
        )

        self.assertRedirects(response, reverse("chores:chore_list"))
        chore = Chore.objects.get()
        self.assertEqual(chore.title, "Wash dishes")
        self.assertEqual(chore.responsible_person, "Alex")
        self.assertEqual(chore.deadline, date(2026, 9, 10))
        self.assertFalse(chore.is_completed)
        self.assertContains(self.client.get(response.url), "Wash dishes")

    def test_invalid_submissions_show_errors_without_saving(self):
        cases = [
            ({}, "title", "This field is required."),
            ({**self.valid_data, "title": "   "}, "title", "This field is required."),
            ({**self.valid_data, "responsible_person": ""}, "responsible_person", "This field is required."),
            ({**self.valid_data, "deadline": ""}, "deadline", "This field is required."),
            ({**self.valid_data, "deadline": "2026-02-30"}, "deadline", "Enter a valid date."),
            ({**self.valid_data, "deadline": "not-a-date"}, "deadline", "Enter a valid date."),
        ]
        for data, field, message in cases:
            with self.subTest(data=data):
                response = self.client.post(self.url, data)
                self.assertEqual(response.status_code, 200)
                self.assertFormError(response.context["form"], field, message)
                self.assertContains(response, message)
                if data.get("title") == "Wash dishes":
                    self.assertContains(response, 'value="Wash dishes"')
                self.assertEqual(Chore.objects.count(), 0)

    def test_submission_requires_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Chore.objects.count(), 0)

        client.get(self.url)
        response = client.post(
            self.url,
            {
                **self.valid_data,
                "csrfmiddlewaretoken": client.cookies["csrftoken"].value,
            },
        )
        self.assertRedirects(response, reverse("chores:chore_list"))
        self.assertEqual(Chore.objects.count(), 1)
