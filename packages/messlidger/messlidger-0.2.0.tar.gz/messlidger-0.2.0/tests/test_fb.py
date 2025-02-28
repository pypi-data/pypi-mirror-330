import unittest.mock

from messlidger.util import FacebookMessage, Messages, ChatterMixin


def test_find_closest_timestamp():
    sent = Messages()
    sent.add(FacebookMessage("a", 2))
    sent.add(FacebookMessage("b", 5))
    sent.add(FacebookMessage("c", 10))
    sent.add(FacebookMessage("d", 23))
    sent.add(FacebookMessage("e", 45))
    m = sent.pop_up_to(15)
    assert m.timestamp_ms == 10
    assert m.mid == "c"
    assert len(sent) == 2
    assert "d" in sent.by_mid
    assert "e" in sent.by_mid

    m = sent.pop_up_to(500)
    assert m.timestamp_ms == 45
    assert m.mid == "e"
    assert len(sent) == 0

    try:
        sent.pop_up_to(5)
    except KeyError as e:
        assert e.args == (5,)

    assert len(sent.by_timestamp_ms) == 0


def test_extensible_media():
    text, urls = ChatterMixin.get_extensible_media(
        unittest.mock.MagicMock,
        """{
      "ZXh0ZW5zaWJsZV9tZXNzYWdlX2F0dGFjaG1lbnQ6ZWUubWlkLiRjQUFBQUFBQlJjclNTc3ZzUUVXTWdiWExjZHU4Sg": {
        "__typename": "ExtensibleMessageAttachment",
        "strong_id__": "ZXh0ZW5zaWJsZV9tZXNzYWdlX2F0dGFjaG1lbnQ6ZWUubWlkLiRjQUFBQUFBQlJjclNTc3ZzUUVXTWdiWExjZHU4Sg",
        "id": "ZXh0ZW5zaWJsZV9tZXNzYWdlX2F0dGFjaG1lbnQ6ZWUubWlkLiRjQUFBQUFBQlJjclNTc3ZzUUVXTWdiWExjZHU4Sg",
        "is_forwardable": true,
        "story_attachment": {
          "url": "https:\\/\\/www.facebook.com\\/gelati.arlequin",
          "title": "Arlequin Gelati",
          "target": {
            "__typename": "User",
            "strong_id__": "100063607510573",
            "id": "100063607510573",
            "friendship_status": "CANNOT_REQUEST"
          },
          "media": {
            "__typename": "GenericAttachmentMedia",
            "imageLarge": {
              "uri": "https:\\/\\/scontent.xx.fbcdn.net\\/v\\/t39.30808-1\\/277748953_396876902442557_5384670406191252860_n.jpg?stp=dst-jpg_p100x100&_nc_cat=102&ccb=1-7&_nc_sid=3a5e4d&_nc_ohc=cMZjLhTqWCoAX8y2EDh&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=00_AfDSMCokBsH3Q377ydXCx5oj4Mz3DdY5liEGlvvQxPA9Ig&oe=6586A89A"
            },
            "image": {
              "uri": "https:\\/\\/scontent.xx.fbcdn.net\\/v\\/t39.30808-1\\/277748953_396876902442557_5384670406191252860_n.jpg?stp=dst-jpg_p100x100&_nc_cat=102&ccb=1-7&_nc_sid=3a5e4d&_nc_ohc=cMZjLhTqWCoAX8y2EDh&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=00_AfDSMCokBsH3Q377ydXCx5oj4Mz3DdY5liEGlvvQxPA9Ig&oe=6586A89A"
            },
            "imageNatural": {
              "uri": "https:\\/\\/scontent.xx.fbcdn.net\\/v\\/t39.30808-1\\/277748953_396876902442557_5384670406191252860_n.jpg?stp=dst-jpg_p100x100&_nc_cat=102&ccb=1-7&_nc_sid=3a5e4d&_nc_ohc=cMZjLhTqWCoAX8y2EDh&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=00_AfDSMCokBsH3Q377ydXCx5oj4Mz3DdY5liEGlvvQxPA9Ig&oe=6586A89A"
            },
            "imageFullScreen": {
              "uri": "https:\\/\\/scontent.xx.fbcdn.net\\/v\\/t39.30808-1\\/277748953_396876902442557_5384670406191252860_n.jpg?stp=dst-jpg_p100x100&_nc_cat=102&ccb=1-7&_nc_sid=3a5e4d&_nc_ohc=cMZjLhTqWCoAX8y2EDh&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=00_AfDSMCokBsH3Q377ydXCx5oj4Mz3DdY5liEGlvvQxPA9Ig&oe=6586A89A"
            },
            "id": ""
          },
          "style_list": [
            "share",
            "fallback"
          ],
          "title_with_entities": {
            "text": "Arlequin Gelati"
          },
          "description": {
            "text": "Glacier artisanal gastronomique"
          },
          "action_links": [
            {
              "__typename": "LinkOpenActionLink",
              "title": "No button"
            }
          ],
          "style_infos": [
            {
              "__typename": "FeedStandardAttachmentStyleInfo"
            },
            {
              "__typename": "FutureOfFeedAttachmentStyleInfo"
            }
          ],
          "deduplication_key": "e9c579b2cb99fcb2f9ddcec4cf4456a6"
        },
        "genie_attachment": {
          "genie_message": {
            "__typename": "User",
            "strong_id__": "100063607510573"
          }
        }
      }
    }
    """,
    )
    assert (
        text
        == "\nhttps://www.facebook.com/gelati.arlequin - Arlequin Gelati - Glacier artisanal gastronomique"
    )
    assert (
        "https://scontent.xx.fbcdn.net/v/t39.30808-1/277748953_396876902442557_5384670406191252860_n.jpg?stp=dst-jpg_p100x100&_nc_cat=102&ccb=1-7&_nc_sid=3a5e4d&_nc_ohc=cMZjLhTqWCoAX8y2EDh&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=00_AfDSMCokBsH3Q377ydXCx5oj4Mz3DdY5liEGlvvQxPA9Ig&oe=6586A89A"
        in urls
    )

    text, urls = ChatterMixin.get_extensible_media(
        unittest.mock.MagicMock,
        """
        {
  "ZXh0ZW5zaWJsZV9tZXNzYWdlX2F0dGFjaG1lbnQ6ZWUubWlkLiRjQUFBN1RSMlYwcWFRSnA1ZC1XSjlWa0duaE1QSw": {
    "typename": "ExtensibleMessageAttachment",
    "strong_id": "ZXh0ZW5zaWJsZV9tZXNzYWdlX2F0dGFjaG1lbnQ6ZWUubWlkLiRjQUFBN1RSMlYwcWFRSnA1ZC1XSjlWa0duaE1QSw",
    "id": "ZXh0ZW5zaWJsZV9tZXNzYWdlX2F0dGFjaG1lbnQ6ZWUubWlkLiRjQUFBN1RSMlYwcWFRSnA1ZC1XSjlWa0duaE1QSw",
    "is_forwardable": true,
    "story_attachment": {
      "url": "fbrpc://facebook/nativethirdparty?app_id=256002347743983&app_name=Facebook+Messenger+for+Android&fallback_url0=https%3A%2F%2Fapps.facebook.com%2Ffbmessenger_android%2F&market_uri=market%3A%2F%2Fdetails%3Fid%3Dcom.facebook.orca%26referrer%3Dutm_source%253Dapps.facebook.com%2526utm_campaign%253Dfb4a%2526utm_content%253D%25257B%252522app%252522%25253A256002347743983%25252C%252522t%252522%25253A1692038403%25252C%252522source%252522%25253Anull%25257D%26app_id%3D256002347743983%26is_vt_odir_eligible%3D0&package_name=com.facebook.orca&tap_behavior=app_fallback_web&target_url=https%3A%2F%2Fwww.amazon.com%2FBCW-1-TLCH-100-Topload-Card-Holder%2Fdp%2FB074VH2VWV%2Fref%3Dasc_df_B074VH2VWV%2F%3Ftag%3Dhyprod-20%26linkCode%3Ddf0%26hvadid%3D241968535606%26hvpos%26hvnetw%3Dg%26hvrand%3D17835882389631259700%26hvpone%26hvptwo%26hvqmt%26hvdev%3Dm%26hvdvcmdl%26hvlocint%26hvlocphy%3D9022116%26hvtargid%3Dpla-600746527901%26psc%3D1&extra_applink_key=al_applink_data&referer_data_key=extras&al_applink_data=%7B%22target_url%22%3A%22https%3A%5C%2F%5C%2Fwww.amazon.com%5C%2FBCW-1-TLCH-100-Topload-Card-Holder%5C%2Fdp%5C%2FB074VH2VWV%5C%2Fref%3Dasc_df_B074VH2VWV%5C%2F%3Ftag%3Dhyprod-20%26linkCode%3Ddf0%26hvadid%3D241968535606%26hvpos%26hvnetw%3Dg%26hvrand%3D17835882389631259700%26hvpone%26hvptwo%26hvqmt%26hvdev%3Dm%26hvdvcmdl%26hvlocint%26hvlocphy%3D9022116%26hvtargid%3Dpla-600746527901%26psc%3D1%22%2C%22extras%22%3A%7B%22fb_app_id%22%3A256002347743983%7D%2C%22referer_app_link%22%3A%7B%22url%22%3A%22fb-messenger%3A%5C%2F%5C%2F%5C%2F%22%2C%22app_name%22%3A%22Messenger%22%2C%22package%22%3A%22com.facebook.orca%22%7D%7D&appsite_data=%7B%22android%22%3A%5B%7B%22is_app_link%22%3Afalse%2C%22app_name%22%3A%22Facebook+Messenger+for+Android%22%2C%22fallback_url%22%3A%22https%3A%5C%2F%5C%2Fapps.facebook.com%5C%2Ffbmessenger_android%5C%2F%22%2C%22market_uri%22%3A%22market%3A%5C%2F%5C%2Fdetails%3Fid%3Dcom.facebook.orca%26referrer%3Dutm_source%5Cu00253Dapps.facebook.com%5Cu002526utm_campaign%5Cu00253Dfb4a%5Cu002526utm_content%5Cu00253D%5Cu0025257B%5Cu00252522app%5Cu00252522%5Cu0025253A256002347743983%5Cu0025252C%5Cu00252522t%5Cu00252522%5Cu0025253A1692038403%5Cu0025252C%5Cu00252522source%5Cu00252522%5Cu0025253Anull%5Cu0025257D%26app_id%3D256002347743983%26is_vt_odir_eligible%3D0%22%2C%22package%22%3A%22com.facebook.orca%22%7D%5D%7D&has_app_link=0",
      "title": "BCW 1-TLCH-100 3X4 Topload Card Holder - Standard",
      "target": {
        "typename": "ExternalUrl",
        "strong_id": "-3483010280417037662",
        "cache_id": "-3483010280417037662"
      },
      "media": {
        "__typename": "GenericAttachmentMedia",
        "imageLarge": {
          "uri": "https://external.xx.fbcdn.net/emg1/v/t13/1740253623741233594?url=https%3A%2F%2Fm.media-amazon.com%2Fimages%2FI%2F51Bdv%252BAUTpL._SR600%252c315_PIWhiteStrip%252cBottomLeft%252c0%252c35_PIStarRatingFOURANDHALF%252cBottomLeft%252c360%252c-6_SR600%252c315_ZA1%25252C081%252c445%252c290%252c400%252c400%252cAmazonEmberBold%252c12%252c4%252c0%252c0%252c5_SCLZZZZZZZ_FMpng_BG255%252c255%252c255.jpg&fb_obo=1&utld=media-amazon.com&stp=c0.5000x0.5000f_dst-emg0_p600x300_q75&ccb=13-1&oh=06_AbHdzVVTmuPsTJnfzPax8Jh8VaeGbFbLUHGZo9IzqUOStQ&oe=64DC008F&_nc_sid=cab974",
          "width": 600,
          "height": 300
        },
        "image": {
          "uri": "https://external.xx.fbcdn.net/emg1/v/t13/1740253623741233594?url=https%3A%2F%2Fm.media-amazon.com%2Fimages%2FI%2F51Bdv%252BAUTpL._SR600%252c315_PIWhiteStrip%252cBottomLeft%252c0%252c35_PIStarRatingFOURANDHALF%252cBottomLeft%252c360%252c-6_SR600%252c315_ZA1%25252C081%252c445%252c290%252c400%252c400%252cAmazonEmberBold%252c12%252c4%252c0%252c0%252c5_SCLZZZZZZZ_FMpng_BG255%252c255%252c255.jpg&fb_obo=1&utld=media-amazon.com&stp=c0.5000x0.5000f_dst-emg0_p600x300_q75&ccb=13-1&oh=06_AbHdzVVTmuPsTJnfzPax8Jh8VaeGbFbLUHGZo9IzqUOStQ&oe=64DC008F&_nc_sid=cab974",
          "width": 600,
          "height": 300
        },
        "imageNatural": {
          "uri": "https://external.xx.fbcdn.net/emg1/v/t13/1740253623741233594?url=https%3A%2F%2Fm.media-amazon.com%2Fimages%2FI%2F51Bdv%252BAUTpL._SR600%252c315_PIWhiteStrip%252cBottomLeft%252c0%252c35_PIStarRatingFOURANDHALF%252cBottomLeft%252c360%252c-6_SR600%252c315_ZA1%25252C081%252c445%252c290%252c400%252c400%252cAmazonEmberBold%252c12%252c4%252c0%252c0%252c5_SCLZZZZZZZ_FMpng_BG255%252c255%252c255.jpg&fb_obo=1&utld=media-amazon.com&stp=c0.5000x0.5000f_dst-emg0_p315x315_q75&ccb=13-1&oh=06_AbHvbZ_aX5MJ_5KwbBv5bMsFjUsNarr3E79K3WUUJ42yOA&oe=64DC008F&_nc_sid=cab974",
          "width": 315,
          "height": 315
        },
        "imageFullScreen": {
          "uri": "https://external.xx.fbcdn.net/emg1/v/t13/1740253623741233594?url=https%3A%2F%2Fm.media-amazon.com%2Fimages%2FI%2F51Bdv%252BAUTpL._SR600%252c315_PIWhiteStrip%252cBottomLeft%252c0%252c35_PIStarRatingFOURANDHALF%252cBottomLeft%252c360%252c-6_SR600%252c315_ZA1%25252C081%252c445%252c290%252c400%252c400%252cAmazonEmberBold%252c12%252c4%252c0%252c0%252c5_SCLZZZZZZZ_FMpng_BG255%252c255%252c255.jpg&fb_obo=1&utld=media-amazon.com&stp=c0.5000x0.5000f_dst-emg0_p315x315_q75&ccb=13-1&oh=06_AbHvbZ_aX5MJ_5KwbBv5bMsFjUsNarr3E79K3WUUJ42yOA&oe=64DC008F&_nc_sid=cab974",
          "width": 315,
          "height": 315
        }
      },
      "style_list": [
        "share",
        "fallback"
      ],
      "title_with_entities": {
        "text": "BCW 1-TLCH-100 3X4 Topload Card Holder - Standard"
      },
      "description": {
        "text": "BCW standard 3x4 top loading card holders are made of high-quality, rigid PVC. These top loading holders are some of the most popular rigid individual card holders in the collectible card industry. Us"
      },
      "source": {
        "text": "amazon.com"
      },
      "attachment_properties": [
        {
          "key": "width",
          "attachment_property_type": "double",
          "value": {
            "text": "600"
          }
        },
        {
          "key": "height",
          "attachment_property_type": "double",
          "value": {
            "text": "315"
          }
        }
      ],
      "style_infos": [
        {
          "__typename": "FeedStandardAttachmentStyleInfo"
        },
        {
          "__typename": "ExternalShareAttachmentStyleInfo"
        },
        {
          "__typename": "FutureOfFeedAttachmentStyleInfo"
        }
      ],
      "deduplication_key": "ee.mid.$cAAA7TR2V0qaQJp5d-WJ9VkGnhMPK"
    },
    "genie_attachment": {
      "genie_message": {
        "typename": "ExternalUrl",
        "strong_id": "-3483010280417037662"
      }
    }
  }
}
        """,
    )
    assert "BCW 1-TLCH-100 3X4 Topload Card Holder - Standard" in text
    assert (
        "fbrpc://facebook/nativethirdparty?app_id=256002347743983&app_name=Facebook+Messenger+for+Android&fallback_url0=https%3A%2F%2Fapps.facebook.com%2Ffbmessenger_android%2F&market_uri=market%3A%2F%2Fdetails%3Fid%3Dcom.facebook.orca%26referrer%3Dutm_source%253Dapps.facebook.com%2526utm_campaign%253Dfb4a%2526utm_content%253D%25257B%252522app%252522%25253A256002347743983%25252C%252522t%252522%25253A1692038403%25252C%252522source%252522%25253Anull%25257D%26app_id%3D256002347743983%26is_vt_odir_eligible%3D0&package_name=com.facebook.orca&tap_behavior=app_fallback_web&target_url=https%3A%2F%2Fwww.amazon.com%2FBCW-1-TLCH-100-Topload-Card-Holder%2Fdp%2FB074VH2VWV%2Fref%3Dasc_df_B074VH2VWV%2F%3Ftag%3Dhyprod-20%26linkCode%3Ddf0%26hvadid%3D241968535606%26hvpos%26hvnetw%3Dg%26hvrand%3D17835882389631259700%26hvpone%26hvptwo%26hvqmt%26hvdev%3Dm%26hvdvcmdl%26hvlocint%26hvlocphy%3D9022116%26hvtargid%3Dpla-600746527901%26psc%3D1&extra_applink_key=al_applink_data&referer_data_key=extras&al_applink_data=%7B%22target_url%22%3A%22https%3A%5C%2F%5C%2Fwww.amazon.com%5C%2FBCW-1-TLCH-100-Topload-Card-Holder%5C%2Fdp%5C%2FB074VH2VWV%5C%2Fref%3Dasc_df_B074VH2VWV%5C%2F%3Ftag%3Dhyprod-20%26linkCode%3Ddf0%26hvadid%3D241968535606%26hvpos%26hvnetw%3Dg%26hvrand%3D17835882389631259700%26hvpone%26hvptwo%26hvqmt%26hvdev%3Dm%26hvdvcmdl%26hvlocint%26hvlocphy%3D9022116%26hvtargid%3Dpla-600746527901%26psc%3D1%22%2C%22extras%22%3A%7B%22fb_app_id%22%3A256002347743983%7D%2C%22referer_app_link%22%3A%7B%22url%22%3A%22fb-messenger%3A%5C%2F%5C%2F%5C%2F%22%2C%22app_name%22%3A%22Messenger%22%2C%22package%22%3A%22com.facebook.orca%22%7D%7D&appsite_data=%7B%22android%22%3A%5B%7B%22is_app_link%22%3Afalse%2C%22app_name%22%3A%22Facebook+Messenger+for+Android%22%2C%22fallback_url%22%3A%22https%3A%5C%2F%5C%2Fapps.facebook.com%5C%2Ffbmessenger_android%5C%2F%22%2C%22market_uri%22%3A%22market%3A%5C%2F%5C%2Fdetails%3Fid%3Dcom.facebook.orca%26referrer%3Dutm_source%5Cu00253Dapps.facebook.com%5Cu002526utm_campaign%5Cu00253Dfb4a%5Cu002526utm_content%5Cu00253D%5Cu0025257B%5Cu00252522app%5Cu00252522%5Cu0025253A256002347743983%5Cu0025252C%5Cu00252522t%5Cu00252522%5Cu0025253A1692038403%5Cu0025252C%5Cu00252522source%5Cu00252522%5Cu0025253Anull%5Cu0025257D%26app_id%3D256002347743983%26is_vt_odir_eligible%3D0%22%2C%22package%22%3A%22com.facebook.orca%22%7D%5D%7D&has_app_link=0"
        in text
    )
    assert (
        "https://external.xx.fbcdn.net/emg1/v/t13/1740253623741233594?url=https%3A%2F%2Fm.media-amazon.com%2Fimages%2FI%2F51Bdv%252BAUTpL._SR600%252c315_PIWhiteStrip%252cBottomLeft%252c0%252c35_PIStarRatingFOURANDHALF%252cBottomLeft%252c360%252c-6_SR600%252c315_ZA1%25252C081%252c445%252c290%252c400%252c400%252cAmazonEmberBold%252c12%252c4%252c0%252c0%252c5_SCLZZZZZZZ_FMpng_BG255%252c255%252c255.jpg&fb_obo=1&utld=media-amazon.com&stp=c0.5000x0.5000f_dst-emg0_p600x300_q75&ccb=13-1&oh=06_AbHdzVVTmuPsTJnfzPax8Jh8VaeGbFbLUHGZo9IzqUOStQ&oe=64DC008F&_nc_sid=cab974"
        in urls
    )
