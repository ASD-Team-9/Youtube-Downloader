﻿using ObjCRuntime;
using UIKit;

namespace YoutubeDownloader;

public class Program
{
	// This is the main entry point of the application.
	static void Main(string[] args)
	{
		// if you want to use a different Application Delegate class from "AppDelegate"
		// you can specify it here.
		int a = 1;
		UIApplication.Main(args, null, typeof(AppDelegate));
	}
}

