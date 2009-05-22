#import <UIKit/UIKit.h>
#import <Foundation/Foundation.h>
@class MainView;
@class Register;
@interface LoggedOutView : UIView <UITextFieldDelegate>{
    IBOutlet MainView *mainview;
    IBOutlet Register *registerView;
}
- (IBAction)registerButtonPushed;
- (IBAction)loginButtonPushed;
@end
