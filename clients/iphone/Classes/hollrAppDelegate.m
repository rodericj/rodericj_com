//
//  hollrAppDelegate.m
//  hollr
//
//  Created by Roderic Campbell on 5/21/09.
//  Copyright Slide 2009. All rights reserved.
//

#import "hollrAppDelegate.h"
#import "hollrViewController.h"

@implementation hollrAppDelegate

@synthesize window;
@synthesize viewController;


- (void)applicationDidFinishLaunching:(UIApplication *)application {    
    
    // Override point for customization after app launch    
    [window addSubview:viewController.view];
    [window makeKeyAndVisible];
}


- (void)dealloc {
    [viewController release];
    [window release];
    [super dealloc];
}


@end
