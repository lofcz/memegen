// Example C# usage for Memegen MCP Server
// Add this to your MCP client code

using System;

public static class MemegenMCPServerFactory
{
    /// <summary>
    /// Creates an MCP server instance for Memegen that runs in Docker.
    /// The Docker image includes both Memegen API and MCP server - just works!
    /// Port is published so you can access generated memes at http://localhost:{port}/images/...
    /// </summary>
    /// <param name="dockerImage">Docker image name (default: lofcz1/memegen-mcp)</param>
    /// <param name="hostPort">Local port to publish (default: 5000). Set to null to not publish port.</param>
    /// <param name="allowedTools">Optional list of allowed tools</param>
    /// <returns>Configured MCPServer instance</returns>
    public static MCPServer MemegenServer(
        string dockerImage = "lofcz1/memegen-mcp",
        int? hostPort = 5000,
        string[]? allowedTools = null)
    {
        var args = new List<string>
        {
            "run",
            "-i",
            "--rm"
        };

        // Only add port mapping if hostPort is specified
        if (hostPort.HasValue)
        {
            args.Add("-p");
            args.Add($"{hostPort.Value}:5000");
        }

        args.Add(dockerImage);

        var server = new MCPServer(
            name: "memegen",
            command: "docker",
            arguments: args.ToArray(),
            allowedTools: allowedTools
        );

        return server;
    }

    /// <summary>
    /// Meme generator using MCP Server Docker image
    /// </summary>
    /// <param name="hostPort">Local port to publish (default: 5000). Use different port if 5000 is already in use.</param>
    /// <param name="allowedTools">Optional list of allowed tools</param>
    /// <returns>Configured MCPServer instance</returns>
    public static MCPServer MemeToolkit(int? hostPort = 5000, string[]? allowedTools = null)
    {
        return MemegenServer("lofcz1/memegen-mcp", hostPort, allowedTools);
    }

    /// <summary>
    /// Creates an MCP server instance for Memegen running locally (no Docker)
    /// </summary>
    /// <param name="pythonPath">Path to Python executable (default: "python")</param>
    /// <param name="mcpServerPath">Path to mcp_server.py</param>
    /// <param name="memegenUrl">URL to Memegen API (default: http://localhost:5000)</param>
    /// <param name="allowedTools">Optional list of allowed tools</param>
    /// <returns>Configured MCPServer instance</returns>
    public static MCPServer MemegenServerLocal(
        string pythonPath = "python",
        string mcpServerPath = "mcp_server.py",
        string memegenUrl = "http://localhost:5000",
        string[]? allowedTools = null)
    {
        var server = new MCPServer(
            name: "memegen",
            command: pythonPath,
            arguments: new[] { mcpServerPath },
            env: new Dictionary<string, string>
            {
                ["MEMEGEN_BASE_URL"] = memegenUrl
            },
            allowedTools: allowedTools
        );

        return server;
    }
}

// Usage example:
/*
// Option 1: Using Docker (recommended - just works, no setup needed!)
var memegenServer = MemegenMCPServerFactory.MemegenServer(
    dockerImage: "lorduser/memegen-mcp:latest"
);

// Option 2: Using local Python (requires Memegen running separately)
var memegenServer = MemegenMCPServerFactory.MemegenServerLocal(
    pythonPath: "python",
    mcpServerPath: @"C:\path\to\memegen\mcp_server.py"
);

// Use the server
var templates = await memegenServer.CallTool("list_templates", new { filter = "coding" });
var memeResponse = await memegenServer.CallTool("generate_meme", new {
    template_id = "fry",
    text_lines = new[] { "Not_sure_if_AI", "Or_really_smart_code" }
});

Console.WriteLine(memeResponse); // URL to generated meme
*/

