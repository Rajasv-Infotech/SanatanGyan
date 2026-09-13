namespace SanatanGyan.Services;

public sealed class BrowserService
{
    public async Task<bool> OpenAsync(string? url)
    {
        if (string.IsNullOrWhiteSpace(url) ||
            !Uri.TryCreate(url, UriKind.Absolute, out var uri) ||
            (uri.Scheme != Uri.UriSchemeHttp && uri.Scheme != Uri.UriSchemeHttps))
        {
            return false;
        }

        try
        {
            await Browser.Default.OpenAsync(uri, BrowserLaunchMode.SystemPreferred);
            return true;
        }
        catch
        {
            return false;
        }
    }
}
