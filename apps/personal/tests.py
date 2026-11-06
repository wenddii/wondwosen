import io
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image
from .models import Activity, ActivityPhoto, ActivityCategory


def create_test_image(color='blue'):
    """Generate a valid in-memory image for testing upload."""
    file = io.BytesIO()
    img = Image.new('RGB', (100, 100), color=color)
    img.save(file, 'jpeg')
    file.seek(0)
    return SimpleUploadedFile('test_photo.jpg', file.read(), content_type='image/jpeg')


class ActivityModelTests(TestCase):
    def setUp(self):
        self.activity = Activity.objects.create(
            title='Boxing Training',
            category=ActivityCategory.BOXING,
            description='Daily boxing workouts and sparring sessions.',
            display_order=1,
            is_active=True
        )

    def test_activity_creation_and_slug(self):
        self.assertEqual(self.activity.slug, 'boxing-training')
        self.assertTrue(self.activity.is_active)
        self.assertEqual(str(self.activity), 'Boxing Training (Boxing)')

    def test_activity_photos_ordering_and_caption(self):
        photo1 = ActivityPhoto.objects.create(
            activity=self.activity,
            image=create_test_image('blue'),
            caption='Sparring session round 3',
            display_order=2
        )
        photo2 = ActivityPhoto.objects.create(
            activity=self.activity,
            image=create_test_image('green'),
            caption='Heavy bag conditioning',
            display_order=1
        )

        ordered = list(self.activity.ordered_photos)
        self.assertEqual(ordered[0], photo2)
        self.assertEqual(ordered[1], photo1)
        self.assertTrue(self.activity.has_photos)

    def test_single_featured_photo_enforcement(self):
        photo1 = ActivityPhoto.objects.create(
            activity=self.activity,
            image=create_test_image('red'),
            caption='First photo',
            is_featured=True,
            display_order=1
        )
        photo2 = ActivityPhoto.objects.create(
            activity=self.activity,
            image=create_test_image('yellow'),
            caption='Second photo',
            is_featured=True,
            display_order=2
        )

        # photo1 should now be unfeatured
        photo1.refresh_from_db()
        photo2.refresh_from_db()
        self.assertFalse(photo1.is_featured)
        self.assertTrue(photo2.is_featured)

        # featured_photo property returns photo2
        self.assertEqual(self.activity.featured_photo, photo2)
        # additional_photos returns photo1
        self.assertIn(photo1, list(self.activity.additional_photos))
        self.assertNotIn(photo2, list(self.activity.additional_photos))

    def test_hide_activity(self):
        self.activity.is_active = False
        self.activity.save()
        active_activities = Activity.objects.filter(is_active=True)
        self.assertNotIn(self.activity, active_activities)

    def test_social_links(self):
        creator_act = Activity.objects.create(
            title='Content Creation',
            category=ActivityCategory.CONTENT_CREATION,
            description='TikTok videos and YouTube technical deep-dives.',
            tiktok_url='https://tiktok.com/@wenddii',
            youtube_url='https://youtube.com/@wenddii',
            display_order=0,
            is_active=True
        )
        self.assertEqual(creator_act.tiktok_url, 'https://tiktok.com/@wenddii')
        self.assertEqual(creator_act.youtube_url, 'https://youtube.com/@wenddii')


class BeyondTheCodeFrontendViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.act1 = Activity.objects.create(
            title='Content Creation',
            slug='content-creation',
            category=ActivityCategory.CONTENT_CREATION,
            description='Creating TikTok and YouTube content and documenting my journey.',
            tiktok_url='https://www.tiktok.com',
            youtube_url='https://www.youtube.com',
            display_order=1,
            is_active=True
        )
        self.act2 = Activity.objects.create(
            title='Hidden Pursuit',
            slug='hidden-pursuit',
            category=ActivityCategory.OTHER,
            description='Should not be visible.',
            display_order=99,
            is_active=False
        )

    def test_index_displays_beyond_the_code(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Beyond the Code')
        self.assertContains(response, 'A little about what I enjoy outside building software.')
        self.assertContains(response, 'Content Creation')
        self.assertContains(response, 'beyond-code-boxes')
        self.assertContains(response, 'js-activity-box')
        # Inactive activity should not appear
        self.assertNotContains(response, 'Hidden Pursuit')
        # Old section should not appear
        self.assertNotContains(response, 'What I Do & Focus On')
        # Lightbox modal should be present in DOM
        self.assertContains(response, 'portfolioLightbox')

    def test_activity_hover_photos_in_index(self):
        photo1 = ActivityPhoto.objects.create(
            activity=self.act1,
            image=create_test_image('blue'),
            caption='Recording a YouTube video in the studio',
            show_on_hover=True,
            display_order=1
        )
        photo2 = ActivityPhoto.objects.create(
            activity=self.act1,
            image=create_test_image('green'),
            caption='Editing timeline screenshot',
            show_on_hover=True,
            display_order=2
        )

        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, photo1.image.url)
        self.assertContains(response, 'Recording a YouTube video in the studio')
        self.assertContains(response, photo2.image.url)
        self.assertContains(response, 'Editing timeline screenshot')
        self.assertContains(response, reverse('personal:detail', kwargs={'slug': self.act1.slug}))

    def test_activity_detail_view(self):
        photo = ActivityPhoto.objects.create(
            activity=self.act1,
            image=create_test_image('red'),
            caption='Detail gallery item',
            display_order=1
        )
        response = self.client.get(reverse('personal:detail', kwargs={'slug': self.act1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Content Creation')
        self.assertContains(response, 'Creating TikTok and YouTube content')
        self.assertContains(response, photo.image.url)
        self.assertContains(response, 'js-lightbox-trigger')
        self.assertContains(response, '← Back to Portfolio')

    def test_show_on_hover_selection(self):
        photo_hover = ActivityPhoto.objects.create(
            activity=self.act1,
            image=create_test_image('purple'),
            caption='Show on hover photo',
            show_on_hover=True,
            display_order=1
        )
        photo_hidden = ActivityPhoto.objects.create(
            activity=self.act1,
            image=create_test_image('orange'),
            caption='Detail only photo',
            show_on_hover=False,
            display_order=2
        )
        hover_list = list(self.act1.hover_photos)
        self.assertIn(photo_hover, hover_list)
        self.assertNotIn(photo_hidden, hover_list)

    def test_personal_moments_slideshow_in_index(self):
        moment1 = ActivityPhoto.objects.create(
            activity=self.act1,
            image=create_test_image('cyan'),
            caption='Sparring session in the ring',
            show_in_moments=True,
            moments_order=1,
            is_published=True
        )
        moment2 = ActivityPhoto.objects.create(
            activity=None,
            image=create_test_image('yellow'),
            caption='University graduation and memorable moments',
            show_in_moments=True,
            moments_order=2,
            is_published=True
        )
        hidden_moment = ActivityPhoto.objects.create(
            activity=self.act1,
            image=create_test_image('black'),
            caption='Unpublished snapshot',
            show_in_moments=True,
            moments_order=3,
            is_published=False
        )

        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Life Beyond the Screen')
        self.assertContains(response, 'moments-slideshow')
        self.assertContains(response, moment1.image.url)
        self.assertContains(response, 'Sparring session in the ring')
        self.assertContains(response, moment2.image.url)
        self.assertContains(response, 'University graduation and memorable moments')
        self.assertNotContains(response, 'Unpublished snapshot')
        self.assertContains(response, 'js-moments-prev')
        self.assertContains(response, 'js-moments-next')

    def test_moments_independent_of_activity_hover(self):
        hover_only = ActivityPhoto.objects.create(
            activity=self.act1,
            image=create_test_image('blue'),
            caption='Hover only preview',
            show_on_hover=True,
            show_in_moments=False
        )
        moments_only = ActivityPhoto.objects.create(
            activity=self.act1,
            image=create_test_image('red'),
            caption='Slideshow only moment',
            show_on_hover=False,
            show_in_moments=True
        )

        self.assertIn(hover_only, list(self.act1.hover_photos))
        self.assertNotIn(moments_only, list(self.act1.hover_photos))

        moments_qs = ActivityPhoto.objects.filter(show_in_moments=True, is_published=True)
        self.assertIn(moments_only, moments_qs)
        self.assertNotIn(hover_only, moments_qs)

    def test_standalone_personal_moment_without_activity(self):
        standalone = ActivityPhoto.objects.create(
            activity=None,
            image=create_test_image('magenta'),
            caption='Public speaking event',
            show_in_moments=True,
            is_published=True
        )
        self.assertIsNone(standalone.activity)
        self.assertIn("Public speaking event", str(standalone))
