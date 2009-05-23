#import <UIKit/UIKit.h>
#import <Foundation/Foundation.h>
@class MainView;
@class Register;
@interface LoggedOutView : UIView <UITextFieldDelegate>{
    IBOutlet MainView *mainview;
    IBOutlet Register *registerView;
	
	IBOutlet UITextField *userName;
	IBOutlet UITextField *password;
	
}
@property (nonatomic, retain) UITextField *userName;
@property (nonatomic, retain) UITextField *password;

- (IBAction)registerButtonPushed;
- (IBAction)loginButtonPushed;
- (IBAction)updateStrings;
@end
