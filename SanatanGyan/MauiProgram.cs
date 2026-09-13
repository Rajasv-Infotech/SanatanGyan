using Microsoft.Extensions.Logging;
using SanatanGyan.Services;

namespace SanatanGyan;

public static class MauiProgram
{
    public static MauiApp CreateMauiApp()
    {
        var builder = MauiApp.CreateBuilder();
        builder.UseMauiApp<App>();
        builder.Services.AddMauiBlazorWebView();
        builder.Services.AddSingleton<KnowledgeService>();
        builder.Services.AddSingleton<BookmarkService>();
        builder.Services.AddSingleton<BrowserService>();
        builder.Services.AddSingleton<LanguageService>();
        builder.Services.AddSingleton<LearningService>();
        builder.Services.AddSingleton<LearningProgressService>();
        builder.Services.AddSingleton<DailySanatanService>();
        builder.Services.AddSingleton<ScriptureService>();
        builder.Services.AddSingleton<PanchangService>();

#if DEBUG
        builder.Services.AddBlazorWebViewDeveloperTools();
        builder.Logging.AddDebug();
#endif
        return builder.Build();
    }
}
