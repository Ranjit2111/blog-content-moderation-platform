#!/usr/bin/env python3
import openapi_client
from openapi_client.models.post_create import PostCreate
from openapi_client.models.post_update import PostUpdate
from openapi_client.rest import ApiException
from pprint import pprint
import time
import sys

def main():
    # Configure API client
    configuration = openapi_client.Configuration(
        host = "http://localhost:8000"  # Update with your actual server URL
    )

    # Initialize API client
    with openapi_client.ApiClient(configuration) as api_client:
        # Create API instances
        posts_api = openapi_client.PostsApi(api_client)
        
        # Step 1: Create a draft post
        print("\n=== Creating a draft post ===")
        try:
            post_create = PostCreate(
                title="Sample Blog Post",
                content="This is a test post to demonstrate the content moderation workflow."
            )
            post = posts_api.create_post_posts_post(post_create)
            print(f"Created draft post with ID: {post.id}")
            print(f"Status: {post.status}")
            
            post_id = post.id
        except ApiException as e:
            print(f"Error creating post: {e}")
            sys.exit(1)
            
        # Step 2: Submit the post for moderation
        print("\n=== Submitting post for moderation ===")
        try:
            moderation_response = posts_api.submit_post_posts_post_id_submit_post(post_id)
            print(f"Moderation response: {moderation_response.status}")
            if moderation_response.reasons:
                print(f"Flagged reasons: {moderation_response.reasons}")
        except ApiException as e:
            print(f"Error submitting post: {e}")
            sys.exit(1)
            
        # Step 3: Get the updated post to check its status
        print("\n=== Checking post status after moderation ===")
        try:
            updated_post = posts_api.get_post_posts_post_id_get(post_id)
            print(f"Post status: {updated_post.status}")
            if updated_post.flagged_reasons:
                print(f"Flagged reasons: {updated_post.flagged_reasons}")
        except ApiException as e:
            print(f"Error getting post: {e}")
            sys.exit(1)
            
        # Step 4: If the post was flagged, update it to address concerns
        if updated_post.status == "flagged" and updated_post.flagged_reasons:
            print("\n=== Updating flagged post ===")
            try:
                post_update = PostUpdate(
                    title=updated_post.title,
                    content="This is an updated post that addresses previous moderation concerns."
                )
                updated_post = posts_api.update_post_posts_post_id_patch(post_id, post_update)
                print(f"Updated post status: {updated_post.status}")
                
                # Re-submit for moderation
                print("\n=== Re-submitting updated post for moderation ===")
                moderation_response = posts_api.submit_post_posts_post_id_submit_post(post_id)
                print(f"Moderation response: {moderation_response.status}")
                
                # Check status again
                updated_post = posts_api.get_post_posts_post_id_get(post_id)
                print(f"Post status after update: {updated_post.status}")
            except ApiException as e:
                print(f"Error updating post: {e}")
                sys.exit(1)
        
        # Step 5: If post is approved, publish it
        # Note: In a real-world scenario, you might need to wait for manual approval
        # This example assumes the post might be auto-approved after submission
        if updated_post.status == "approved":
            print("\n=== Publishing approved post ===")
            try:
                published_post = posts_api.publish_post_posts_post_id_publish_patch(post_id)
                print(f"Post published successfully!")
                print(f"Final status: {published_post.status}")
            except ApiException as e:
                print(f"Error publishing post: {e}")
                sys.exit(1)
        else:
            print("\n=== Post is not yet approved for publishing ===")
            print(f"Current status: {updated_post.status}")
            
        # Step 6: List all posts to verify our post is there
        print("\n=== Listing all posts ===")
        try:
            all_posts = posts_api.list_posts_posts_get()
            print(f"Found {len(all_posts)} posts:")
            for p in all_posts:
                print(f"ID: {p.id}, Title: {p.title}, Status: {p.status}")
                
            # Additionally, demonstrate filtering by status
            print("\n=== Listing draft posts ===")
            draft_posts = posts_api.list_posts_posts_get(status="draft")
            print(f"Found {len(draft_posts)} draft posts")
            
            if updated_post.status == "published":
                print("\n=== Listing published posts ===")
                published_posts = posts_api.list_posts_posts_get(status="published")
                print(f"Found {len(published_posts)} published posts")
                for p in published_posts:
                    print(f"ID: {p.id}, Title: {p.title}")
        except ApiException as e:
            print(f"Error listing posts: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()