#import "LoggedOutView.h"
#import "MainView.h"
@implementation LoggedOutView
- (IBAction)registerButtonPushed {
    NSLog(@"registerButtonPushed");
	[mainview switchToRegisterView];

}
- (IBAction)loginButtonPushed {
    NSLog(@"login Button Pushed");
}
@end
