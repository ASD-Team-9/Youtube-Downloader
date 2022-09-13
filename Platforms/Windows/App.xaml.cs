using Microsoft.UI;
using Microsoft.UI.Windowing;
using Windows.Graphics;

namespace YoutubeDownloader.WinUI;

/// <summary>
/// Provides application-specific behavior to supplement the default Application class.
/// </summary>
public partial class App : MauiWinUIApplication
{
    private const int WindowWidth = 1280;
    private const int WindowHeight = 720;

    /// <summary>
    /// Initializes the singleton application object.  This is the first line of authored code
    /// executed, and as such is the logical equivalent of main() or WinMain().
    /// </summary>
    public App()
    {
        InitializeComponent();

        Microsoft.Maui.Handlers.WindowHandler.Mapper.AppendToMapping(nameof(IWindow), (handler, view) =>
        {
#if WINDOWS
            var mauiWindow = handler.VirtualView;
            var nativeWindow = handler.PlatformView;

            nativeWindow.Activate();
            IntPtr windowHandle = WinRT.Interop.WindowNative.GetWindowHandle(nativeWindow);
            WindowId windowId = Win32Interop.GetWindowIdFromWindow(windowHandle);

            AppWindow appWindow = AppWindow.GetFromWindowId(windowId);
            if (appWindow.Presenter is OverlappedPresenter p)
            {
                p.IsResizable = false;
            }
            appWindow.Resize(new(WindowWidth, WindowHeight));
#endif
        });
    }

    protected override MauiApp CreateMauiApp() => MauiProgram.CreateMauiApp();
}