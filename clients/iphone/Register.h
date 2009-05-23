#import <UIKit/UIKit.h>
#import <Foundation/Foundation.h>

@interface Register : UIView <UITextFieldDelegate>{
	IBOutlet UITextField *userName;
	IBOutlet UITextField *email;
	IBOutlet UITextField *firstName;
	IBOutlet UITextField *lastName;
	IBOutlet UITextField *password;
	IBOutlet UITextField *confirmPassword;


}
@property (nonatomic, retain) UITextField *userName;
@property (nonatomic, retain) UITextField *email;
@property (nonatomic, retain) UITextField *firstName;
@property (nonatomic, retain) UITextField *lastName;
@property (nonatomic, retain) UITextField *password;
@property (nonatomic, retain) UITextField *confirmPassword;


- (IBAction)sendRegistrationInfo;
- (IBAction)updateStrings;

@end