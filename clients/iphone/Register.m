#import "Register.h"

@implementation Register
- (IBAction)sendRegistrationInfo {
    
}
- (void)updateStrings{
	NSLog(userName.text);
	NSLog(email.text);
	NSLog(firstName.text);
	NSLog(password.text);
	NSLog(confirmPassword.text);
}
- (BOOL)textFieldShouldClear:(UITextField *)textField {
	return YES;
}

- (BOOL) textFieldShouldBeginEditing:(UITextField *)textField{
	//Begin aniimations to move Text Fields into view
	[UIView beginAnimations:@"moveField" context:nil];
	[UIView setAnimationDelegate:self];
	[UIView setAnimationDuration:0.5];
	[UIView setAnimationCurve:UIViewAnimationCurveEaseInOut];
	textField.frame =CGRectMake(textField.frame.origin.x,
								 textField.frame.origin.y-100, 
								 textField.frame.size.width, 
								 textField.frame.size.height);
	[UIView commitAnimations];
	return YES;
}
	
- (BOOL)textFieldShouldReturn:(UITextField *)theTextField {
	NSLog(@"hit return maybe?");
	[theTextField resignFirstResponder];
	return NO;
}

@end
