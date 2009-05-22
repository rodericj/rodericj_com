#import <UIKit/UIKit.h>
#import <Foundation/Foundation.h>

@class LoggedInView;
@class LoggedOutView;
@class Register;
@interface MainView :UIView {
	IBOutlet LoggedInView *loggedInView;
	IBOutlet LoggedOutView *loggedOutView;
	IBOutlet Register *registerView;

}
-(IBOutlet)switchToRegisterView;

@end
