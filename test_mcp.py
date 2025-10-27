#!/usr/bin/env python3
"""
Test script for Memegen MCP Server

This script tests the MCP server functionality without needing an MCP client.
"""

import asyncio
import json
import httpx

MEMEGEN_BASE_URL = "http://localhost:5000"


async def test_memegen_connection():
    """Test if Memegen server is accessible."""
    print("Testing connection to Memegen server...")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{MEMEGEN_BASE_URL}/templates/")
            if response.status_code == 200:
                print("✅ Memegen server is running and accessible")
                return True
            else:
                print(f"❌ Memegen server returned status code {response.status_code}")
                return False
    except httpx.ConnectError:
        print(f"❌ Cannot connect to Memegen server at {MEMEGEN_BASE_URL}")
        print("   Make sure to run 'start.bat' or 'start_app.bat' first!")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def test_list_templates():
    """Test listing templates."""
    print("\n" + "="*60)
    print("Test: List Templates")
    print("="*60)
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{MEMEGEN_BASE_URL}/templates/")
            response.raise_for_status()
            templates = response.json()
            
            print(f"✅ Found {len(templates)} templates")
            print("\nFirst 5 templates:")
            for template in templates[:5]:
                print(f"  • {template['name']} (ID: {template['id']})")
            
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def test_get_template():
    """Test getting a specific template."""
    print("\n" + "="*60)
    print("Test: Get Template Details")
    print("="*60)
    
    template_id = "fry"
    print(f"Getting details for template: {template_id}")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{MEMEGEN_BASE_URL}/templates/{template_id}")
            response.raise_for_status()
            template = response.json()
            
            print(f"✅ Template found: {template['name']}")
            print(f"   Lines: {template['lines']}")
            print(f"   Example: {template['example']['url']}")
            
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def test_generate_meme():
    """Test generating a meme."""
    print("\n" + "="*60)
    print("Test: Generate Meme")
    print("="*60)
    
    template_id = "fry"
    text_lines = ["Testing_MCP_Server", "Seems_to_work"]
    extension = "png"
    
    print(f"Generating meme with template: {template_id}")
    print(f"Text lines: {text_lines}")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            text_path = "/".join(text_lines)
            url = f"{MEMEGEN_BASE_URL}/images/{template_id}/{text_path}.{extension}"
            
            response = await client.head(url, follow_redirects=True)
            
            if response.status_code == 200:
                print(f"✅ Meme generated successfully!")
                print(f"   URL: {response.url}")
                return True
            else:
                print(f"❌ Failed with status code {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def test_search_examples():
    """Test searching for examples."""
    print("\n" + "="*60)
    print("Test: Search Meme Examples")
    print("="*60)
    
    query = "code"
    print(f"Searching for examples matching: {query}")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{MEMEGEN_BASE_URL}/images/", params={"filter": query})
            response.raise_for_status()
            examples = response.json()
            
            print(f"✅ Found {len(examples)} examples")
            if examples:
                print("\nFirst 3 examples:")
                for example in examples[:3]:
                    print(f"  • {example['template']}: {example['url']}")
            
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def main():
    """Run all tests."""
    print("=" * 60)
    print("Memegen MCP Server Test Suite")
    print("=" * 60)
    
    # Test connection first
    if not await test_memegen_connection():
        print("\n❌ Cannot proceed without Memegen server running.")
        print("   Please start Memegen with: start.bat or start_app.bat")
        return
    
    # Run all tests
    tests = [
        test_list_templates,
        test_get_template,
        test_generate_meme,
        test_search_examples,
    ]
    
    results = []
    for test in tests:
        result = await test()
        results.append(result)
        await asyncio.sleep(0.5)  # Small delay between tests
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ All tests passed! MCP server is ready to use.")
        print("\nNext steps:")
        print("1. Run: install_mcp.bat (if not already done)")
        print("2. Run: start_mcp.bat")
        print("3. Configure your MCP client (see MCP_README.md)")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Check the output above.")


if __name__ == "__main__":
    asyncio.run(main())

