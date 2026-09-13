using Android.App;
using Android.Content.PM;
using Android.OS;
using AndroidX.Core.View;

namespace SanatanGyan;

[Activity(
    Theme = "@style/Maui.SplashTheme",
    MainLauncher = true,
    LaunchMode = LaunchMode.SingleTop,
    ConfigurationChanges = ConfigChanges.ScreenSize | ConfigChanges.Orientation | ConfigChanges.UiMode |
                           ConfigChanges.ScreenLayout | ConfigChanges.SmallestScreenSize | ConfigChanges.Density)]
public class MainActivity : MauiAppCompatActivity
{
    protected override void OnCreate(Bundle? savedInstanceState)
    {
        base.OnCreate(savedInstanceState);
        // Android 15+ can draw app content edge-to-edge by default. Keep the Blazor
        // surface inside system bars so the Sanatan header is never hidden behind
        // the status bar/camera cutout. CSS safe-area padding remains as a fallback.
        WindowCompat.SetDecorFitsSystemWindows(Window, true);
    }
}
