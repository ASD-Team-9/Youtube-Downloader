namespace YoutubeDownloader;

public partial class MainPage : ContentPage
{
	int count = 0;

	public MainPage()
	{
		InitializeComponent();
	}

	private void OnCounterClicked(object sender, EventArgs e)
	{
		count++;

		if (count == 1)
			CounterBtn.Text = $"Search {count} time";
		else
			CounterBtn.Text = $"Search {count} times";

		SemanticScreenReader.Announce(CounterBtn.Text);
	}
}


