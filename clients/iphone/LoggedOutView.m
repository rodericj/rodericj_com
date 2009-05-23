#import "LoggedOutView.h"
#import "MainView.h"
@implementation LoggedOutView
- (IBAction)registerButtonPushed {
    NSLog(@"registerButtonPushed");
	[mainview switchToRegisterView];

}
- (IBAction)loginButtonPushed {
    NSLog(@"login Button Pushed");
	NSLog(userName.text);
	NSLog(password.text);
}

- (void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event
{
    // Dismiss the keyboard when the view outside the text field is touched.
	//Going through each text box may not be the best way to do this.
	[userName resignFirstResponder];
	[password resignFirstResponder];
    // Revert the text field to the previous value.
   // textField.text = self.string; 
   // [super touchesBegan:touches withEvent:event];
}

- (IBAction)updateStrings{
	NSLog(@"updateString in LoggedOutView");
	NSLog(userName.text);
	NSLog(password.text);
}

@end
