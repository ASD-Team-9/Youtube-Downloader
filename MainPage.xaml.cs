using Microsoft.Maui.Platform;

namespace YoutubeDownloader;

public partial class MainPage : ContentPage
{
	public List<Video> downloadingVideos = new();

	public MainPage()
	{
		InitializeComponent();
		VideoDownloadListView.SetBinding(Label.TextProperty, "Video");
		VideoDownloadListView.BindingContext = downloadingVideos;
	}

	private void OnCounterClicked(object sender, EventArgs e)
	{
		downloadingVideos.Add(new("YouTube Video Name here."));
        CounterBtn.Text = "Huh";
    }
}