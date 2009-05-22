//
//  hollrAppDelegate.h
//  hollr
//
//  Created by Roderic Campbell on 5/21/09.
//  Copyright Slide 2009. All rights reserved.
//

#import <UIKit/UIKit.h>

@class hollrViewController;

@interface hollrAppDelegate : NSObject <UIApplicationDelegate> {
    UIWindow *window;
    hollrViewController *viewController;
}

@property (nonatomic, retain) IBOutlet UIWindow *window;
@property (nonatomic, retain) IBOutlet hollrViewController *viewController;

@end

